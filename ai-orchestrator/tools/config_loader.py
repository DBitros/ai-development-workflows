"""
Configuration loader with support for extending base configs.

Loads YAML configuration files and handles the 'extends' directive to
support platform-specific configs that extend a generic base.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def deep_merge(base: Dict[Any, Any], override: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Dictionary with values to override/add

    Returns:
        Merged dictionary
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = deep_merge(result[key], value)
        else:
            # Override value
            result[key] = value

    return result


def load_config(config_path: str, base_dir: Optional[str] = None) -> Dict[Any, Any]:
    """
    Load configuration from YAML file with support for 'extends' directive.

    Args:
        config_path: Path to config file (can be relative or absolute)
        base_dir: Base directory for resolving relative paths (default: config file's dir)

    Returns:
        Merged configuration dictionary

    Example:
        # agents-trademe.yaml contains:
        # extends: "agents-generic.yaml"
        # agents:
        #   architect:
        #     name: "TradeMe iOS Architect"

        config = load_config("config/agents-trademe.yaml")
        # Result has generic config merged with TradeMe-specific overrides
    """
    config_file = Path(config_path)

    # Determine base directory for resolving relative paths
    if base_dir is None:
        base_dir = config_file.parent

    # Load the config file
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # Check if this config extends another
    if 'extends' in config:
        base_config_path = config.pop('extends')  # Remove 'extends' key

        # Resolve path relative to current config's directory
        if not Path(base_config_path).is_absolute():
            base_config_path = base_dir / base_config_path

        # Recursively load base config
        base_config = load_config(str(base_config_path), base_dir)

        # Merge base config with current config (current overrides base)
        config = deep_merge(base_config, config)

    return config


def load_config_by_name(config_name: str,
                        config_dir: str = "config") -> Dict[Any, Any]:
    """
    Load configuration by name (without .yaml extension).

    Args:
        config_name: Config name like "generic", "trademe", or "agents-trademe"
        config_dir: Directory containing config files (default: "config")

    Returns:
        Configuration dictionary

    Examples:
        >>> config = load_config_by_name("trademe")
        >>> config = load_config_by_name("generic")
        >>> config = load_config_by_name("agents-trademe", config_dir="config")
    """
    # Add prefix if not present
    if not config_name.startswith("agents-"):
        config_name = f"agents-{config_name}"

    # Add extension if not present
    if not config_name.endswith(".yaml"):
        config_name = f"{config_name}.yaml"

    config_path = Path(config_dir) / config_name

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    return load_config(str(config_path))


def get_available_configs(config_dir: str = "config") -> list:
    """
    Get list of available configuration names.

    Args:
        config_dir: Directory containing config files (default: "config")

    Returns:
        List of config names (without agents- prefix and .yaml extension)

    Examples:
        >>> get_available_configs()
        ['generic', 'trademe']
    """
    config_path = Path(config_dir)
    config_files = config_path.glob("agents-*.yaml")

    # Extract names without prefix and extension
    names = []
    for file in config_files:
        name = file.stem  # Remove .yaml
        name = name.replace("agents-", "")  # Remove agents- prefix
        names.append(name)

    return sorted(names)


def get_config_value(config: Dict[Any, Any],
                     key_path: str,
                     default: Any = None) -> Any:
    """
    Get a nested configuration value using dot notation.

    Args:
        config: Configuration dictionary
        key_path: Dot-separated path like "agents.architect.name"
        default: Default value if key not found

    Returns:
        Configuration value or default

    Examples:
        >>> config = {"agents": {"architect": {"name": "Software Architect"}}}
        >>> get_config_value(config, "agents.architect.name")
        'Software Architect'

        >>> get_config_value(config, "agents.missing.key", default="N/A")
        'N/A'
    """
    keys = key_path.split(".")
    value = config

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value


if __name__ == "__main__":
    print("Configuration Loader Test")
    print("=" * 80)

    # List available configs
    print("\nAvailable configs:")
    configs = get_available_configs()
    for config_name in configs:
        print(f"  - {config_name}")

    # Test loading generic config
    print("\n" + "=" * 80)
    print("Loading generic config:")
    print("=" * 80)
    generic_config = load_config_by_name("generic")
    print(f"Architect name: {get_config_value(generic_config, 'agents.architect.name')}")
    print(f"Work folder: {get_config_value(generic_config, 'paths.work_folder')}")

    # Test loading trademe config (extends generic)
    print("\n" + "=" * 80)
    print("Loading TradeMe config (extends generic):")
    print("=" * 80)
    trademe_config = load_config_by_name("trademe")
    print(f"Architect name: {get_config_value(trademe_config, 'agents.architect.name')}")
    print(f"Work folder: {get_config_value(trademe_config, 'paths.work_folder')}")
    print(f"Target project: {get_config_value(trademe_config, 'paths.target_project')}")

    # Show TradeMe-specific values
    print(f"\nTradeMe-specific architecture rules:")
    arch_rules = get_config_value(trademe_config, 'architecture_rules', {})
    print(f"  - Universal API enabled: {arch_rules.get('universal_api', {}).get('enabled')}")
    print(f"  - Module pattern: {arch_rules.get('module_structure', {}).get('pattern')}")

    print("\n" + "=" * 80)
