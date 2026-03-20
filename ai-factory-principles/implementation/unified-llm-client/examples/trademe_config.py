"""
Example: Using Unified LLM Client with Trade Me LiteLLM proxy.

This shows how to automatically load configuration from Claude Code settings.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from unified_llm import Client, generate
from unified_llm.adapters import AnthropicAdapter
from unified_llm.config import ConfigLoader


async def main():
    """Demonstrate auto-configuration from Claude settings."""

    print("=" * 70)
    print("Trade Me Configuration Example")
    print("=" * 70)
    print()

    # Load configuration from ~/.claude/settings.json
    print("Loading configuration from Claude Code settings...")
    config = ConfigLoader.from_claude_settings()

    print(f"✅ Loaded configuration:")
    print(f"   Base URL: {config.get('ANTHROPIC_BASE_URL')}")
    print(f"   API Key: {config.get('ANTHROPIC_API_KEY', '')[:20]}...")
    print()

    # Create client with Trade Me configuration
    adapter = AnthropicAdapter(
        api_key=config["ANTHROPIC_API_KEY"],
        base_url=config["ANTHROPIC_BASE_URL"].rstrip('/'),
        timeout=30.0
    )

    client = Client(
        providers={"anthropic": adapter},
        default_provider="anthropic"
    )

    # Test with different models
    models_to_test = [
        ("claude-haiku-4-5", "Fast & cheap"),
        ("claude-sonnet-4-5", "Balanced"),
        ("claude-opus-4-6", "Most capable"),
    ]

    for model, description in models_to_test:
        print(f"Testing {model} ({description})")
        print("-" * 70)

        try:
            response = await generate(
                model=model,
                prompt="In one word, what is the capital of New Zealand?",
                client=client
            )

            print(f"✅ Response: {response.text}")
            print(f"   Tokens: {response.usage.total_tokens}")
            print()

        except Exception as e:
            print(f"❌ Error: {e}")
            print()

    # Demonstrate the model mapping helper
    print("Model Name Mappings:")
    print("-" * 70)
    mappings = ConfigLoader.get_model_mapping()
    for alias, model in mappings.items():
        print(f"  {alias:15} → {model}")
    print()

    # Cleanup
    await client.close()

    print("=" * 70)
    print("Configuration example completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
