"""
Basic coding agent example.

Demonstrates autonomous agent that can read, write, and execute code.
"""

import asyncio
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'unified-llm-client', 'src'))

from agent import Session, SessionConfig, create_standard_tools
from unified_llm import Client
from unified_llm.adapters import AnthropicAdapter
from unified_llm.config import ConfigLoader


async def main():
    """Run a basic coding agent."""

    print("=" * 70)
    print("Basic Coding Agent Example")
    print("=" * 70)
    print()

    # Load configuration from Claude settings
    config = ConfigLoader.from_claude_settings()

    # Create LLM client
    adapter = AnthropicAdapter(
        api_key=config["ANTHROPIC_API_KEY"],
        base_url=config["ANTHROPIC_BASE_URL"].rstrip('/'),
        timeout=30.0
    )

    llm_client = Client(
        providers={"anthropic": adapter},
        default_provider="anthropic"
    )

    # Create agent session
    session = Session(
        llm_client=llm_client,
        provider="anthropic",
        model="claude-sonnet-4-5",  # Balanced model
        config=SessionConfig(
            max_tool_rounds_per_input=20,
            enable_loop_detection=True
        ),
        working_directory="/tmp/agent_test"
    )

    # Register tools
    session.tool_registry = create_standard_tools().tools

    print("🤖 Agent initialized!")
    print(f"   Model: claude-sonnet-4-5")
    print(f"   Working dir: /tmp/agent_test")
    print(f"   Tools: {len(session.tool_registry)}")
    print()

    # Task 1: Create a simple Python file
    print("Task 1: Create a prime number checker")
    print("-" * 70)

    task1 = """
    Create a Python file called prime_checker.py that contains a function
    is_prime(n) which returns True if n is prime, False otherwise.

    The function should handle edge cases:
    - Numbers less than 2 are not prime
    - 2 is prime
    - Even numbers > 2 are not prime
    - Check odd divisors up to sqrt(n)
    """

    result1 = await session.submit(task1)
    print(f"Agent response: {result1}")
    print()

    # Show events
    print("Events emitted:")
    for event in session.get_events():
        print(f"  [{event.kind.value}] at {event.timestamp.strftime('%H:%M:%S')}")
    print()

    # Task 2: Test the file
    print("Task 2: Test the prime checker")
    print("-" * 70)

    task2 = """
    Read the prime_checker.py file and verify it looks correct.
    Then create a test that checks:
    - is_prime(2) returns True
    - is_prime(17) returns True
    - is_prime(4) returns False
    - is_prime(1) returns False
    """

    result2 = await session.submit(task2)
    print(f"Agent response: {result2}")
    print()

    # Cleanup
    await session.close()
    await llm_client.close()

    print("=" * 70)
    print("Basic agent example completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
