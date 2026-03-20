#!/bin/bash
# Setup Trade Me LiteLLM proxy environment variables

export ANTHROPIC_API_KEY="sk-xRNpmJnYBicomozd2NTrvA"
export ANTHROPIC_BASE_URL="https://litellm-proxy.ds-staff-gen-ai.stg.app.trade.me/"

echo "✅ Trade Me LiteLLM proxy environment configured!"
echo ""
echo "Available models:"
echo "  - claude-sonnet-4-5[1m]"
echo "  - claude-haiku-4-5[1m]"
echo "  - claude-opus-4-6[1m]"
echo ""
echo "Run tests with:"
echo "  python test_trademe.py"
