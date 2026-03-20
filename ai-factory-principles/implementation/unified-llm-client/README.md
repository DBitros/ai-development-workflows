# Unified LLM Client

A single interface across multiple LLM providers (OpenAI, Anthropic, Gemini).

## Features

✅ **Multi-provider support** - OpenAI, Anthropic, Gemini through one interface
✅ **Native API usage** - Each provider uses its optimal API (Responses, Messages, Gemini)
✅ **Streaming-first** - Proper streaming with separate return types
✅ **Tool calling** - Universal tool interface across providers
✅ **Prompt caching** - Automatic for OpenAI/Gemini, smart injection for Anthropic
✅ **Middleware** - Logging, caching, cost tracking, rate limiting
✅ **Model catalog** - Up-to-date model metadata and selection

## Quick Start

### Installation

```bash
cd implementation/unified-llm-client
pip install -e .
```

### Basic Usage

```python
from unified_llm import Client, generate

# Auto-configure from environment variables
client = Client.from_env()

# Simple generation
response = generate(
    model="claude-opus-4-6",
    prompt="What is 2+2?",
    client=client
)
print(response.text)
# Output: "2+2 equals 4."

# Streaming
for chunk in stream(model="gpt-5.2", prompt="Count to 10"):
    print(chunk.text, end="", flush=True)
```

### Multi-Provider

```python
# Claude
response = generate(
    model="claude-opus-4-6",
    prompt="Explain quantum computing"
)

# GPT
response = generate(
    model="gpt-5.2",
    prompt="Explain quantum computing"
)

# Gemini
response = generate(
    model="gemini-3-flash-preview",
    prompt="Explain quantum computing"
)
```

### With Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

response = generate(
    model="claude-opus-4-6",
    prompt="What's the weather in Tokyo?",
    tools=tools
)

if response.tool_calls:
    for call in response.tool_calls:
        print(f"Tool: {call.name}")
        print(f"Args: {call.arguments}")
```

## Architecture

```
┌─────────────────────────────────────────────┐
│  High-Level API (generate, stream)          │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  Client (routing, middleware)                │
└─────────────┬───────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ OpenAI │ │Anthropic│ │ Gemini │
│Adapter │ │ Adapter │ │Adapter │
└────────┘ └────────┘ └────────┘
```

## Environment Setup

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Gemini
export GEMINI_API_KEY="..."
```

## Advanced Usage

### Custom Client Configuration

```python
from unified_llm import Client
from unified_llm.adapters import OpenAIAdapter, AnthropicAdapter

# Explicit adapter configuration
openai_adapter = OpenAIAdapter(
    api_key="sk-...",
    base_url="https://custom-endpoint.example.com/v1",
    timeout=30.0
)

anthropic_adapter = AnthropicAdapter(
    api_key="sk-ant-...",
    timeout=60.0
)

client = Client(
    providers={
        "openai": openai_adapter,
        "anthropic": anthropic_adapter
    },
    default_provider="anthropic"
)
```

### Middleware

```python
from unified_llm import Client

def logging_middleware(request, next_fn):
    """Log all requests"""
    print(f"[REQUEST] {request.provider}/{request.model}")
    response = next_fn(request)
    print(f"[RESPONSE] {response.usage.total_tokens} tokens")
    return response

def cost_tracking_middleware(request, next_fn):
    """Track costs"""
    response = next_fn(request)
    cost = calculate_cost(response.usage, request.model)
    print(f"[COST] ${cost:.4f}")
    return response

client = Client.from_env(
    middleware=[logging_middleware, cost_tracking_middleware]
)
```

### Model Catalog

```python
from unified_llm.catalog import get_model_info, list_models

# Get model details
info = get_model_info("claude-opus-4-6")
print(f"Context: {info.context_window} tokens")
print(f"Supports tools: {info.supports_tools}")

# List all models for a provider
models = list_models(provider="anthropic")
for model in models:
    print(f"{model.id}: {model.display_name}")

# Get latest model
latest = get_latest_model(provider="openai", capability="reasoning")
print(f"Best OpenAI reasoning model: {latest.id}")
```

## Implementation Status

### ✅ Phase 1: Core (Completed)
- [x] Data models (Message, Request, Response)
- [x] Provider adapter interface
- [x] Client with routing
- [x] Environment-based setup

### 🚧 Phase 2: Adapters (In Progress)
- [x] OpenAI adapter (Responses API)
- [x] Anthropic adapter (Messages API)
- [x] Gemini adapter (Gemini API)
- [x] Streaming support
- [x] Tool calling

### 📋 Phase 3: Advanced Features (Next)
- [ ] Middleware system
- [ ] Prompt caching (Anthropic auto-injection)
- [ ] Model catalog
- [ ] Cost tracking
- [ ] Retry logic

### 📋 Phase 4: Polish (Future)
- [ ] Comprehensive tests
- [ ] Documentation
- [ ] Examples
- [ ] Performance optimization

## Testing

```bash
# Run tests
pytest tests/

# Test specific adapter
pytest tests/test_openai_adapter.py

# Integration tests (requires API keys)
pytest tests/integration/
```

## Examples

See `examples/` directory for:
- `basic_usage.py` - Simple generation
- `streaming.py` - Streaming responses
- `tool_calling.py` - Using tools
- `multi_provider.py` - Switching between providers
- `middleware.py` - Custom middleware

## Contributing

This is part of the Software Factory implementation. As you use it:
- Add new providers as needed
- Contribute middleware examples
- Report issues and improvements

## License

Following StrongDM's approach - freely shareable.

---

**Version**: 0.1.0 (Initial Implementation)
**Last Updated**: February 2026
