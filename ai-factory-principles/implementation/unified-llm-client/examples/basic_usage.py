"""
Basic usage example for the Unified LLM Client.

This demonstrates the simplest way to use the client.
"""

import asyncio
import os
from unified_llm import generate, Client


async def main():
    """Run basic examples."""

    # Ensure API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        print("export ANTHROPIC_API_KEY='sk-ant-...'")
        return

    print("=" * 60)
    print("Unified LLM Client - Basic Usage Examples")
    print("=" * 60)
    print()

    # Example 1: Simple generation
    print("Example 1: Simple Generation")
    print("-" * 60)
    response = await generate(
        model="claude-opus-4-6",
        prompt="What is 2+2? Answer in one sentence."
    )
    print(f"Response: {response.text}")
    print(f"Tokens: {response.usage.total_tokens}")
    print()

    # Example 2: With system prompt
    print("Example 2: With System Prompt")
    print("-" * 60)
    response = await generate(
        model="claude-sonnet-4-5",
        system="You are a helpful math tutor. Always show your work.",
        prompt="What is 15 × 23?"
    )
    print(f"Response: {response.text}")
    print()

    # Example 3: Multi-turn conversation
    print("Example 3: Multi-Turn Conversation")
    print("-" * 60)
    from unified_llm import Message

    messages = [
        Message.user("My name is Alice."),
        Message.assistant("Hello Alice! How can I help you today?"),
        Message.user("What's my name?")
    ]

    response = await generate(
        model="claude-sonnet-4-5",
        messages=messages
    )
    print(f"Response: {response.text}")
    print()

    # Example 4: Tool calling
    print("Example 4: Tool Calling")
    print("-" * 60)

    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'Tokyo', 'London')"
                    }
                },
                "required": ["location"]
            }
        }
    ]

    response = await generate(
        model="claude-opus-4-6",
        prompt="What's the weather like in Tokyo?",
        tools=tools
    )

    if response.tool_calls:
        print("Tool calls:")
        for call in response.tool_calls:
            print(f"  - {call.name}({call.arguments})")
    else:
        print(f"Response: {response.text}")
    print()

    # Example 5: Using explicit client configuration
    print("Example 5: Explicit Client Configuration")
    print("-" * 60)

    from unified_llm.adapters import AnthropicAdapter

    # Create custom adapter
    adapter = AnthropicAdapter(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        timeout=30.0
    )

    # Create client with custom configuration
    client = Client(
        providers={"anthropic": adapter},
        default_provider="anthropic"
    )

    response = await generate(
        model="claude-haiku-4-5",
        prompt="Say hello in Japanese.",
        client=client
    )
    print(f"Response: {response.text}")
    print()

    # Cleanup
    await client.close()

    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
