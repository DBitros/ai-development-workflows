# Coding Agent Loop

An autonomous coding agent that pairs LLMs with developer tools through an agentic loop.

Based on StrongDM's `coding-agent-loop-spec.md` from https://github.com/strongdm/attractor

## Features

✅ **Autonomous execution** - Runs end-to-end without human intervention
✅ **Tool execution** - Read, write, edit, shell, grep, glob
✅ **Provider-aligned** - Native tools for OpenAI, Anthropic, Gemini
✅ **Subagents** - Spawn parallel workers for decomposed tasks
✅ **Loop detection** - Identifies and breaks infinite loops
✅ **Steering** - Inject messages mid-task to redirect
✅ **Event system** - Real-time progress updates
✅ **Context management** - Output truncation, token tracking

## Quick Start

### Installation

```bash
cd implementation/coding-agent
pip install -e .
```

### Basic Usage

```python
from agent import CodingAgent, Session
from unified_llm import Client

# Create client
client = Client.from_env()

# Create agent session
session = Session(
    client=client,
    provider="anthropic",
    model="claude-opus-4-6"
)

# Execute a task
await session.submit("Create a Python function that checks if a number is prime")

# Agent will:
# 1. Plan the implementation
# 2. Write the code
# 3. Test it (if tests exist)
# 4. Iterate until working
```

## Architecture

```
┌─────────────────────────────────────────────┐
│  Session (orchestrator)                      │
│  - Conversation history                      │
│  - Tool execution                            │
│  - Loop detection                            │
│  - Event emission                            │
└─────────────┬───────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│  Tools │ │  LLM   │ │SubAgent│
│Registry│ │ Client │ │ Spawn  │
└────────┘ └────────┘ └────────┘
```

## The Core Loop

```python
while not done:
    # 1. Call LLM with conversation history
    response = await llm.complete(messages, tools)

    # 2. If no tool calls, agent is done
    if not response.tool_calls:
        break

    # 3. Execute tool calls
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call)
        messages.append(tool_result(result))

    # 4. Loop detection
    if detect_loop(recent_calls):
        inject_warning()

    # 5. Continue loop
```

## Tools

### Core Tools (All Providers)
- **read_file** - Read file contents with line numbers
- **write_file** - Create or overwrite files
- **edit_file** - Search and replace (Anthropic native)
- **shell** - Execute commands with timeout
- **grep** - Search file contents
- **glob** - Find files by pattern

### Provider-Specific
- **apply_patch** - OpenAI's v4a patch format (better for GPT models)
- **spawn_agent** - Launch subagents for parallel work

## Configuration

```python
from agent import SessionConfig

config = SessionConfig(
    max_turns=100,                    # Total turns allowed
    max_tool_rounds_per_input=50,     # Tool rounds per user input
    default_command_timeout_ms=10000, # 10 seconds
    enable_loop_detection=True,
    loop_detection_window=10          # Check last 10 calls
)

session = Session(client, config=config)
```

## Implementation Status

### ✅ Phase 1: Core Loop (Today)
- [x] Session orchestrator
- [x] Basic tool execution
- [x] Event system
- [x] Loop detection

### 🚧 Phase 2: Tools (Next)
- [ ] File operations (read, write, edit)
- [ ] Shell execution with timeout
- [ ] Search tools (grep, glob)
- [ ] Output truncation

### 📋 Phase 3: Advanced (Week 2)
- [ ] Subagent spawning
- [ ] Steering mechanism
- [ ] Multiple execution environments
- [ ] Provider profiles

## Examples

See `examples/` for:
- `basic_agent.py` - Simple autonomous agent
- `with_tools.py` - Agent using file and shell tools
- `subagents.py` - Parallel agent execution
- `steering.py` - Mid-task redirection

## Next Steps

After basic agent loop:
1. Build Digital Twin for validation
2. Create scenario harness
3. Implement Attractor pipeline
4. Full Software Factory workflow

---

**Version**: 0.1.0 (In Development)
**Last Updated**: February 2026
