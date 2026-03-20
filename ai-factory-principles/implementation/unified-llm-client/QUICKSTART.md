# Quick Start Guide

Get up and running with the Unified LLM Client in 5 minutes.

## Installation

```bash
cd ~/Development/ai-tools/ai-factory-principles/implementation/unified-llm-client

# Install in development mode
pip install -e .
```

## Set Up API Keys

```bash
# Anthropic (required for current implementation)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI (coming soon)
export OPENAI_API_KEY="sk-..."

# Gemini (coming soon)
export GEMINI_API_KEY="..."
```

## Your First Request

Create a file called `test.py`:

```python
import asyncio
from unified_llm import generate

async def main():
    response = await generate(
        model="claude-opus-4-6",
        prompt="What is 2+2?"
    )
    print(response.text)

asyncio.run(main())
```

Run it:

```bash
python test.py
```

Expected output:
```
2+2 equals 4.
```

## Next Steps

### Try Streaming

```python
from unified_llm import stream

async def stream_example():
    async for chunk in stream(
        model="claude-sonnet-4-5",
        prompt="Count to 10"
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
```

### Use Tools

```python
response = await generate(
    model="claude-opus-4-6",
    prompt="What's the weather in Tokyo?",
    tools=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }]
)

if response.tool_calls:
    for call in response.tool_calls:
        print(f"Tool: {call.name}")
        print(f"Args: {call.arguments}")
```

### Multi-Turn Conversation

```python
from unified_llm import Message

messages = [
    Message.user("My name is Alice."),
    Message.assistant("Hello Alice!"),
    Message.user("What's my name?")
]

response = await generate(
    model="claude-sonnet-4-5",
    messages=messages
)
```

## Run Examples

```bash
# Basic usage
python examples/basic_usage.py

# Streaming
python examples/streaming.py
```

## Implementation Status

### ✅ Working Now
- [x] Anthropic adapter (Messages API)
- [x] Streaming support
- [x] Tool calling
- [x] Prompt caching (automatic)
- [x] Multi-turn conversations
- [x] System prompts

### 🚧 Coming Soon
- [ ] OpenAI adapter (Responses API)
- [ ] Gemini adapter (Gemini API)
- [ ] Middleware system
- [ ] Cost tracking
- [ ] Retry logic

## Troubleshooting

### Import Error

```
ModuleNotFoundError: No module named 'unified_llm'
```

**Solution**: Install in development mode:
```bash
pip install -e .
```

### API Key Error

```
ValueError: No API keys found in environment
```

**Solution**: Set your API key:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### httpx Not Found

```
ModuleNotFoundError: No module named 'httpx'
```

**Solution**: Install dependencies:
```bash
pip install httpx
```

## What's Next?

1. **Read the README** for detailed documentation
2. **Check examples/** for more usage patterns
3. **Integrate with your agents** using the unified interface
4. **Build your Software Factory!**

---

**Questions?** Check the [main README](./README.md) or the [Software Factory docs](../../README.md).
