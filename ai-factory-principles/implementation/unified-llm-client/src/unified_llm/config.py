"""
Configuration helpers for loading settings from Claude Code and environment.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Load configuration from Claude Code settings and environment."""

    @staticmethod
    def from_claude_settings(settings_path: Optional[str] = None) -> Dict[str, str]:
        """
        Load configuration from Claude Code settings.json.

        Args:
            settings_path: Path to settings.json (defaults to ~/.claude/settings.json)

        Returns:
            Dict of environment variables suitable for LLM client

        Example:
            >>> config = ConfigLoader.from_claude_settings()
            >>> print(config["ANTHROPIC_API_KEY"])
            'sk-xRNpmJnYBicomozd2NTrvA'
        """
        if settings_path is None:
            settings_path = Path.home() / ".claude" / "settings.json"
        else:
            settings_path = Path(settings_path)

        if not settings_path.exists():
            raise FileNotFoundError(f"Claude settings not found at {settings_path}")

        with open(settings_path, 'r') as f:
            settings = json.load(f)

        env = settings.get("env", {})

        # Map Claude Code env vars to standard names
        config = {}

        # Anthropic
        if "ANTHROPIC_AUTH_TOKEN" in env:
            config["ANTHROPIC_API_KEY"] = env["ANTHROPIC_AUTH_TOKEN"]
        if "ANTHROPIC_BASE_URL" in env:
            config["ANTHROPIC_BASE_URL"] = env["ANTHROPIC_BASE_URL"]

        # Model defaults
        if "ANTHROPIC_DEFAULT_SONNET_MODEL" in env:
            config["DEFAULT_SONNET_MODEL"] = env["ANTHROPIC_DEFAULT_SONNET_MODEL"]
        if "ANTHROPIC_DEFAULT_HAIKU_MODEL" in env:
            config["DEFAULT_HAIKU_MODEL"] = env["ANTHROPIC_DEFAULT_HAIKU_MODEL"]
        if "ANTHROPIC_DEFAULT_OPUS_MODEL" in env:
            config["DEFAULT_OPUS_MODEL"] = env["ANTHROPIC_DEFAULT_OPUS_MODEL"]

        return config

    @staticmethod
    def apply_to_env(config: Dict[str, str]):
        """
        Apply configuration to os.environ.

        Args:
            config: Configuration dict from from_claude_settings()

        Example:
            >>> config = ConfigLoader.from_claude_settings()
            >>> ConfigLoader.apply_to_env(config)
            >>> # Now Client.from_env() will use these settings
        """
        for key, value in config.items():
            os.environ[key] = value

    @staticmethod
    def load_and_apply() -> Dict[str, str]:
        """
        Load from Claude settings and apply to environment (one-liner).

        Returns:
            The loaded configuration

        Example:
            >>> ConfigLoader.load_and_apply()
            >>> client = Client.from_env()  # Uses Claude Code settings!
        """
        config = ConfigLoader.from_claude_settings()
        ConfigLoader.apply_to_env(config)
        return config

    @staticmethod
    def get_model_mapping() -> Dict[str, str]:
        """
        Get model name mapping for LiteLLM LiteLLM proxy.

        The proxy uses different model names than direct Anthropic API.
        This mapping helps convert between formats.

        Returns:
            Dict mapping display name to proxy model ID
        """
        return {
            # Standard names → Proxy names
            "haiku": "claude-haiku-4-5",
            "sonnet": "claude-sonnet-4-5",
            "opus": "claude-opus-4-6",

            # With 1m context
            "haiku-1m": "claude-haiku-4-5[1m]",
            "sonnet-1m": "claude-sonnet-4-5[1m]",
            "opus-1m": "claude-opus-4-6[1m]",

            # Gemini (bonus)
            "gemini-pro": "gemini-2-5-pro",
            "gemini-flash": "gemini-3-flash-preview",
        }
