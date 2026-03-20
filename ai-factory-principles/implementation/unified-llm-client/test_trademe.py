"""
Test the Unified LLM Client with Trade Me's LiteLLM proxy.

Uses configuration from ~/.claude/settings.json
"""

import asyncio
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from unified_llm import Client
from unified_llm.adapters import AnthropicAdapter
from unified_llm import generate


async def test_trademe_proxy():
    """Test with Trade Me's LiteLLM proxy configuration."""

    print("=" * 70)
    print("Testing Unified LLM Client with Trade Me LiteLLM Proxy")
    print("=" * 70)
    print()

    # Configuration from your ~/.claude/settings.json
    auth_token = "sk-xRNpmJnYBicomozd2NTrvA"
    base_url = "https://litellm-proxy.ds-staff-gen-ai.stg.app.trade.me/"

    # Available models (from LiteLLM proxy /models endpoint)
    models = [
        "claude-sonnet-4-5",     # No [1m] suffix for proxy!
        "claude-haiku-4-5",
        "claude-opus-4-6",
        "gemini-2-5-pro",        # Bonus: Gemini also available!
        "gemini-3-flash-preview"
    ]

    print(f"🔗 Base URL: {base_url}")
    print(f"🔑 Auth Token: {auth_token[:20]}...")
    print(f"📦 Available Models: {', '.join(models)}")
    print()

    # Create adapter with Trade Me configuration
    adapter = AnthropicAdapter(
        api_key=auth_token,  # LiteLLM accepts this as auth
        base_url=base_url.rstrip('/'),  # Remove trailing slash
        timeout=30.0
    )

    # Create client
    client = Client(
        providers={"anthropic": adapter},
        default_provider="anthropic"
    )

    # Test 1: Simple generation with Haiku (fastest)
    print("Test 1: Simple Generation (Haiku)")
    print("-" * 70)
    try:
        response = await generate(
            model="claude-haiku-4-5",  # Works with proxy!
            prompt="What is 2+2? Answer in one sentence.",
            client=client
        )
        print(f"✅ Success!")
        print(f"Response: {response.text}")
        print(f"Tokens: {response.usage.total_tokens}")
        if response.usage.cache_read_tokens > 0:
            print(f"Cache hits: {response.usage.cache_read_tokens} tokens cached!")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

    # Test 2: With system prompt (Sonnet)
    print("Test 2: With System Prompt (Sonnet)")
    print("-" * 70)
    try:
        response = await generate(
            model="claude-sonnet-4-5",
            system="You are a helpful math tutor.",
            prompt="What is 15 × 23? Show your work.",
            client=client
        )
        print(f"✅ Success!")
        print(f"Response: {response.text}")
        print(f"Cache stats:")
        print(f"  - Cache read: {response.usage.cache_read_tokens} tokens")
        print(f"  - Cache write: {response.usage.cache_write_tokens} tokens")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

    # Test 3: Multi-turn conversation
    print("Test 3: Multi-Turn Conversation (Sonnet)")
    print("-" * 70)
    try:
        from unified_llm import Message

        messages = [
            Message.user("My name is Alice."),
            Message.assistant("Hello Alice! How can I help you today?"),
            Message.user("What's my name?")
        ]

        response = await generate(
            model="claude-sonnet-4-5",
            messages=messages,
            client=client
        )
        print(f"✅ Success!")
        print(f"Response: {response.text}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

    # Test 4: Tool calling (Opus for best results)
    print("Test 4: Tool Calling (Opus)")
    print("-" * 70)
    try:
        tools = [
            {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        }
                    },
                    "required": ["location"]
                }
            }
        ]

        response = await generate(
            model="claude-opus-4-6",
            prompt="What's the weather like in Auckland?",
            tools=tools,
            client=client
        )

        print(f"✅ Success!")
        if response.tool_calls:
            print(f"Tool calls made:")
            for call in response.tool_calls:
                print(f"  - {call.name}({call.arguments})")
        else:
            print(f"Response: {response.text}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

    # Test 5: Streaming
    print("Test 5: Streaming (Haiku)")
    print("-" * 70)
    try:
        from unified_llm import stream

        print("Response: ", end="", flush=True)
        async for chunk in stream(
            model="claude-haiku-4-5",
            prompt="Count from 1 to 5, one number per line.",
            client=client
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
        print(f"✅ Streaming worked!")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

    # Cleanup
    await client.close()

    print("=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_trademe_proxy())
