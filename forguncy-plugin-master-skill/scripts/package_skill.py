#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python scripts/package_skill.py <path/to/skill-folder> [output-directory]
"""

import sys
import zipfile
import os
from pathlib import Path
from quick_validate import validate_skill


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    # Run validation
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # Create the .skill file
    try:
        print(f"📦 Creating package at: {skill_filename}")
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Files to exclude from the package (dev tools)
            EXCLUDED_FILES = {'package_skill.py', 'package_skill.ps1', 'quick_validate.py'}

            # Walk through the skill directory
            for root, dirs, files in os.walk(skill_path):
                # Exclude .git, .trae, __pycache__, etc.
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if file.startswith('.') or file.endswith('.pyc') or file.endswith('.skill'):
                        continue
                    
                    if file in EXCLUDED_FILES:
                        continue
                        
                    file_path = Path(root) / file
                    # Calculate relative path for zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ Error creating .skill file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        # Default to current directory if no args provided
        cwd = Path.cwd()
        # If we are inside 'scripts', assume skill root is parent
        if cwd.name == 'scripts':
            skill_path = cwd.parent
        # If we are in skill root (contain SKILL.md)
        elif (cwd / 'SKILL.md').exists():
            skill_path = cwd
        else:
            print("Usage: python scripts/package_skill.py <path/to/skill-folder> [output-directory]")
            sys.exit(1)
    else:
        skill_path = sys.argv[1]

    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    package_skill(skill_path, output_dir)


if __name__ == "__main__":
    main()
