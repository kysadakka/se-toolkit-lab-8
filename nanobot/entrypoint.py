#!/usr/bin/env python3
"""
Entrypoint for nanobot Docker container.

Resolves environment variables in config.json at runtime,
then launches nanobot gateway.
"""

import json
import os
import re
import sys


def resolve_env_vars(config: dict) -> dict:
    """Replace ${VAR_NAME} placeholders with environment variable values."""
    config_str = json.dumps(config)

    # Find all ${VAR_NAME} patterns
    pattern = r'\$\{([^}]+)\}'

    def replace_var(match):
        var_name = match.group(1)
        value = os.environ.get(var_name, '')
        if not value:
            print(f"Warning: Environment variable {var_name} is not set", file=sys.stderr)
        return value

    resolved_str = re.sub(pattern, replace_var, config_str)
    return json.loads(resolved_str)


def main():
    # Paths
    # In Docker, config is mounted from workspace at /workspace/nanobot/config.json
    # In local dev, it's at /app/nanobot/config.json
    workspace_config_path = '/workspace/nanobot/config.json'
    local_config_path = '/app/nanobot/config.json'
    
    config_path = workspace_config_path if os.path.exists(workspace_config_path) else local_config_path
    
    resolved_path = '/app/nanobot/config.resolved.json'
    workspace_path = '/workspace'

    # Read config template
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Resolve environment variables
    resolved_config = resolve_env_vars(config)

    # Write resolved config
    with open(resolved_path, 'w') as f:
        json.dump(resolved_config, f, indent=2)

    print(f"Resolved config written to {resolved_path}")
    print(f"Using config from: {config_path}")

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace_path])


if __name__ == "__main__":
    main()
