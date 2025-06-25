#!/usr/bin/env python3
"""
Generate requirements.txt file from dependencies.toml for a specific profile.
Usage: python generate_requirements.py <profile_name> [output_file]
"""

import sys
import argparse
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("Error: Neither tomllib (Python 3.11+) nor tomli is available", file=sys.stderr)
        sys.exit(1)


def resolve_profile(config, profile_name, resolved=None):
    """Recursively resolve dependencies for a profile, handling inheritance."""
    if resolved is None:
        resolved = set()
    
    if profile_name in resolved:
        return []
    
    resolved.add(profile_name)
    
    if profile_name not in config['profiles']:
        print(f'Error: Profile {profile_name} not found', file=sys.stderr)
        print(f'Available profiles: {list(config["profiles"].keys())}', file=sys.stderr)
        sys.exit(1)
    
    profile = config['profiles'][profile_name]
    dependencies = profile.get('dependencies', [])
    
    # Handle extends
    extends = profile.get('extends', [])
    if isinstance(extends, str):
        extends = [extends]
    
    for extend_profile in extends:
        extended_deps = resolve_profile(config, extend_profile, resolved.copy())
        dependencies = extended_deps + dependencies
    
    return dependencies


def main():
    parser = argparse.ArgumentParser(description='Generate requirements.txt from dependencies.toml')
    parser.add_argument('profile', help='Profile name to generate requirements for')
    parser.add_argument('output', nargs='?', default='/tmp/requirements.txt', 
                       help='Output file path (default: /tmp/requirements.txt)')
    parser.add_argument('--toml-file', default='dependencies.toml',
                       help='Path to dependencies.toml file')
    
    args = parser.parse_args()
    
    try:
        # Read TOML file
        with open(args.toml_file, 'rb') as f:
            config = tomllib.load(f)
        
        # Resolve dependencies for the specified profile
        dependencies = resolve_profile(config, args.profile)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_deps = []
        for dep in dependencies:
            if dep not in seen:
                seen.add(dep)
                unique_deps.append(dep)
        
        # Write to requirements file
        with open(args.output, 'w') as f:
            for dep in unique_deps:
                f.write(dep + '\n')
        
        print(f'Generated requirements for profile: {args.profile}')
        print(f'Total dependencies: {len(unique_deps)}')
        print(f'Output file: {args.output}')
        
    except FileNotFoundError as e:
        print(f'Error: File not found - {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main() 