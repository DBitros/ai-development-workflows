"""
Core Session class for the coding agent loop.

Based on StrongDM's coding-agent-loop-spec.md
"""

import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, AsyncIterator
from datetime import datetime
from enum import Enum

# Will import from unified_llm when installed
# from unified_llm import Client, Message, ToolCall, ToolResult


class SessionState(str, Enum):
    """Session lifecycle states."""
    IDLE = "idle"                    # Waiting for input
    PROCESSING = "processing"        # Running agentic loop
    AWAITING_INPUT = "awaiting_input"  # Model asked user a question
    CLOSED = "closed"                # Session terminated


class EventKind(str, Enum):
    """Event types emitted by the session."""
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    USER_INPUT = "user_input"
    ASSISTANT_TEXT_START = "assistant_text_start"
    ASSISTANT_TEXT_DELTA = "assistant_text_delta"
    ASSISTANT_TEXT_END = "assistant_text_end"
    TOOL_CALL_START = "tool_call_start"
    TOOL_CALL_OUTPUT_DELTA = "tool_call_output_delta"
    TOOL_CALL_END = "tool_call_end"
    STEERING_INJECTED = "steering_injected"
    TURN_LIMIT = "turn_limit"
    LOOP_DETECTION = "loop_detection"
    ERROR = "error"
    WARNING = "warning"


@dataclass
class SessionEvent:
    """Event emitted during session execution."""
    kind: EventKind
    timestamp: datetime
    session_id: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionConfig:
    """Configuration for session behavior."""
    max_turns: int = 0                      # 0 = unlimited
    max_tool_rounds_per_input: int = 0      # 0 = unlimited
    default_command_timeout_ms: int = 10000  # 10 seconds
    max_command_timeout_ms: int = 600000    # 10 minutes
    reasoning_effort: Optional[str] = None  # "low", "medium", "high"
    enable_loop_detection: bool = True
    loop_detection_window: int = 10
    max_subagent_depth: int = 1

    # Tool output limits (in characters)
    tool_output_limits: Dict[str, int] = field(default_factory=lambda: {
        "read_file": 50000,
        "shell": 30000,
        "grep": 20000,
        "glob": 20000,
        "edit_file": 10000,
        "write_file": 1000,
    })


class Session:
    """
    Core orchestrator for the coding agent loop.

    Manages conversation state, executes tool calls, detects loops,
    and emits events for monitoring.
    """

    def __init__(
        self,
        llm_client: Any,  # unified_llm.Client
        provider: str,
        model: str,
        config: Optional[SessionConfig] = None,
        working_directory: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())
        self.llm_client = llm_client
        self.provider = provider
        self.model = model
        self.config = config or SessionConfig()
        self.working_directory = working_directory or os.getcwd()

        # Session state
        self.state = SessionState.IDLE
        self.history: List[Any] = []  # List[Turn]
        self.steering_queue: List[str] = []
        self.followup_queue: List[str] = []
        self.events: List[SessionEvent] = []

        # Tool execution
        self.tool_registry = {}  # Will be populated with tools
        self.tool_call_history: List[Dict[str, Any]] = []  # For loop detection

        # Emit session start
        self._emit(EventKind.SESSION_START, session_id=self.id)

    def _emit(self, kind: EventKind, **data):
        """Emit an event."""
        event = SessionEvent(
            kind=kind,
            timestamp=datetime.now(),
            session_id=self.id,
            data=data
        )
        self.events.append(event)
        return event

    async def submit(self, user_input: str) -> str:
        """
        Submit user input and run the agentic loop until completion.

        Args:
            user_input: The user's message/task

        Returns:
            The agent's final text response

        Raises:
            Exception: On unrecoverable errors
        """
        self.state = SessionState.PROCESSING
        self._emit(EventKind.USER_INPUT, content=user_input)

        # Add user message to history
        # TODO: Use proper Turn types
        self.history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })

        # Drain steering queue
        self._drain_steering()

        round_count = 0

        # THE CORE AGENTIC LOOP
        while True:
            # 1. Check limits
            if self.config.max_tool_rounds_per_input > 0 and round_count >= self.config.max_tool_rounds_per_input:
                self._emit(EventKind.TURN_LIMIT, round=round_count)
                break

            if self.config.max_turns > 0 and len(self.history) >= self.config.max_turns:
                self._emit(EventKind.TURN_LIMIT, total_turns=len(self.history))
                break

            # 2. Build LLM request
            # TODO: Implement proper message conversion
            messages = self._build_messages()

            # 3. Call LLM
            try:
                from unified_llm import generate

                response = await generate(
                    model=self.model,
                    messages=messages,
                    tools=self._get_tool_definitions() if self.tool_registry else None,
                    client=self.llm_client
                )

                # Record assistant turn
                self.history.append({
                    "role": "assistant",
                    "content": response.text,
                    "tool_calls": response.tool_calls,
                    "usage": response.usage,
                    "timestamp": datetime.now()
                })

                self._emit(
                    EventKind.ASSISTANT_TEXT_END,
                    text=response.text,
                    usage=response.usage.__dict__ if response.usage else {}
                )

                # 4. If no tool calls, natural completion
                if not response.tool_calls:
                    break

                # 5. Execute tool calls
                round_count += 1
                results = await self._execute_tool_calls(response.tool_calls)

                # Record tool results
                self.history.append({
                    "role": "tool",
                    "results": results,
                    "timestamp": datetime.now()
                })

                # 6. Drain steering
                self._drain_steering()

                # 7. Loop detection
                if self.config.enable_loop_detection:
                    if self._detect_loop():
                        warning = (
                            f"Loop detected: the last {self.config.loop_detection_window} "
                            "tool calls follow a repeating pattern. Try a different approach."
                        )
                        self.history.append({
                            "role": "steering",
                            "content": warning,
                            "timestamp": datetime.now()
                        })
                        self._emit(EventKind.LOOP_DETECTION, message=warning)

            except Exception as e:
                self._emit(EventKind.ERROR, error=str(e))
                raise

        # Process follow-ups if any
        if self.followup_queue:
            next_input = self.followup_queue.pop(0)
            return await self.submit(next_input)

        self.state = SessionState.IDLE
        self._emit(EventKind.SESSION_END)

        # Return final text
        return self._get_last_assistant_text()

    def _build_messages(self) -> List[Any]:
        """Convert history to Message objects for LLM."""
        from unified_llm import Message

        messages = []
        for turn in self.history:
            role = turn["role"]
            if role == "user":
                messages.append(Message.user(turn["content"]))
            elif role == "assistant":
                # TODO: Handle tool calls in content
                messages.append(Message.assistant(turn.get("content", "")))
            elif role == "tool":
                # TODO: Convert tool results to proper format
                pass
            elif role == "steering":
                messages.append(Message.user(turn["content"]))

        return messages

    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get tool definitions for LLM."""
        return [
            {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for name, tool in self.tool_registry.items()
        ]

    async def _execute_tool_calls(self, tool_calls: List[Any]) -> List[Any]:
        """Execute tool calls and return results."""
        results = []

        for tool_call in tool_calls:
            self._emit(
                EventKind.TOOL_CALL_START,
                tool_name=tool_call.name,
                call_id=tool_call.id
            )

            # Track for loop detection
            self.tool_call_history.append({
                "name": tool_call.name,
                "arguments": tool_call.arguments,
                "timestamp": datetime.now()
            })

            # Execute tool
            if tool_call.name in self.tool_registry:
                tool = self.tool_registry[tool_call.name]
                try:
                    # Call tool executor
                    output = await tool["executor"](tool_call.arguments, self)

                    # Truncate output
                    truncated = self._truncate_output(output, tool_call.name)

                    self._emit(
                        EventKind.TOOL_CALL_END,
                        call_id=tool_call.id,
                        output=output  # Full output in event
                    )

                    results.append({
                        "tool_call_id": tool_call.id,
                        "content": truncated,  # Truncated to LLM
                        "is_error": False
                    })

                except Exception as e:
                    error_msg = f"Tool error ({tool_call.name}): {str(e)}"
                    self._emit(
                        EventKind.TOOL_CALL_END,
                        call_id=tool_call.id,
                        error=error_msg
                    )
                    results.append({
                        "tool_call_id": tool_call.id,
                        "content": error_msg,
                        "is_error": True
                    })
            else:
                error_msg = f"Unknown tool: {tool_call.name}"
                self._emit(EventKind.ERROR, error=error_msg)
                results.append({
                    "tool_call_id": tool_call.id,
                    "content": error_msg,
                    "is_error": True
                })

        return results

    def _truncate_output(self, output: str, tool_name: str) -> str:
        """Truncate tool output to configured limits."""
        max_chars = self.config.tool_output_limits.get(tool_name, 30000)

        if len(output) <= max_chars:
            return output

        # Head/tail split
        half = max_chars // 2
        removed = len(output) - max_chars

        return (
            output[:half] +
            f"\n\n[WARNING: Tool output was truncated. "
            f"{removed} characters were removed from the middle. "
            f"The full output is available in the event stream.]\n\n" +
            output[-half:]
        )

    def _drain_steering(self):
        """Inject all pending steering messages."""
        while self.steering_queue:
            msg = self.steering_queue.pop(0)
            self.history.append({
                "role": "steering",
                "content": msg,
                "timestamp": datetime.now()
            })
            self._emit(EventKind.STEERING_INJECTED, content=msg)

    def _detect_loop(self) -> bool:
        """Detect if recent tool calls form a repeating pattern."""
        window = self.config.loop_detection_window
        if len(self.tool_call_history) < window:
            return False

        recent = self.tool_call_history[-window:]

        # Create signatures (name + arguments)
        signatures = [
            f"{call['name']}:{hash(str(call['arguments']))}"
            for call in recent
        ]

        # Check for patterns of length 1, 2, or 3
        for pattern_len in [1, 2, 3]:
            if window % pattern_len != 0:
                continue

            pattern = signatures[:pattern_len]
            all_match = True

            for i in range(pattern_len, window, pattern_len):
                if signatures[i:i+pattern_len] != pattern:
                    all_match = False
                    break

            if all_match:
                return True

        return False

    def _get_last_assistant_text(self) -> str:
        """Get the last assistant text response."""
        for turn in reversed(self.history):
            if turn["role"] == "assistant":
                return turn.get("content", "")
        return ""

    def steer(self, message: str):
        """
        Queue a message to inject between tool rounds.

        Args:
            message: Steering message to inject
        """
        self.steering_queue.append(message)

    def follow_up(self, message: str):
        """
        Queue a message to process after current input completes.

        Args:
            message: Follow-up message to process
        """
        self.followup_queue.append(message)

    def get_events(self, kind: Optional[EventKind] = None) -> List[SessionEvent]:
        """
        Get events, optionally filtered by kind.

        Args:
            kind: Event type to filter by

        Returns:
            List of events
        """
        if kind is None:
            return self.events
        return [e for e in self.events if e.kind == kind]

    async def close(self):
        """Close the session and cleanup resources."""
        self.state = SessionState.CLOSED
        self._emit(EventKind.SESSION_END, final_state=self.state.value)
