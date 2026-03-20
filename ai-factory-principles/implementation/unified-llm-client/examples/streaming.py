"""
Streaming example for the Unified LLM Client.

Demonstrates real-time token streaming.
"""

import asyncio
import os
from unified_llm import stream


async def main():
    """Run streaming examples."""

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    print("=" * 60)
    print("Unified LLM Client - Streaming Examples")
    print("=" * 60)
    print()

    # Example 1: Simple streaming
    print("Example 1: Simple Streaming")
    print("-" * 60)
    print("Response: ", end="", flush=True)

    async for chunk in stream(
        model="claude-sonnet-4-5",
        prompt="Count from 1 to 10, one number per line."
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")

    # Example 2: Streaming with system prompt
    print("Example 2: Streaming Story")
    print("-" * 60)
    print("Story: ", end="", flush=True)

    async for chunk in stream(
        model="claude-opus-4-6",
        system="You are a creative short story writer.",
        prompt="Write a 3-sentence story about a robot learning to paint."
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")

    # Example 3: Collecting stream with usage tracking
    print("Example 3: Stream with Usage Tracking")
    print("-" * 60)

    collected_text = []
    total_tokens = 0

    async for chunk in stream(
        model="claude-haiku-4-5",
        prompt="Explain quantum computing in 2 sentences."
    ):
        if chunk.text:
            collected_text.append(chunk.text)
            print(chunk.text, end="", flush=True)
        if chunk.usage:
            total_tokens = chunk.usage.total_tokens

    print()
    print(f"\nTotal text length: {len(''.join(collected_text))} chars")
    print(f"Total tokens: {total_tokens}")
    print()

    print("=" * 60)
    print("All streaming examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
