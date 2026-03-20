#!/usr/bin/env python3
"""Renames a GDExtension throughout the project.

Usage:
    python tools/rename_extension.py <old_name> <new_name>

Example:
    python tools/rename_extension.py myextension my_game

This will:
    - Rename the CMake target
    - Rename the init function (<old_name>_init -> <new_name>_init)
    - Update library paths in the .gdextension file
    - Rename the .gdextension file itself
    - Update the project name in the top-level CMakeLists.txt
"""

import sys
import os
import re
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEARCH_DIRS = [
    "cpp",
    "godot/project",
]

SEARCH_EXTENSIONS = {".cpp", ".hpp", ".h", ".txt", ".gdextension", ".cmake"}

TOP_LEVEL_CMAKE = "CMakeLists.txt"


def validate_name(name: str, label: str) -> None:
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print(f"Error: {label} '{name}' is not a valid name.")
        print("Use lowercase letters, numbers, and underscores. Must start with a letter.")
        sys.exit(1)


def find_files() -> list[str]:
    """Find all files that could contain extension references."""
    files = []
    for search_dir in SEARCH_DIRS:
        full_dir = os.path.join(PROJECT_ROOT, search_dir)
        for root, _, filenames in os.walk(full_dir):
            for filename in filenames:
                if os.path.splitext(filename)[1] in SEARCH_EXTENSIONS:
                    files.append(os.path.join(root, filename))

    top_cmake = os.path.join(PROJECT_ROOT, TOP_LEVEL_CMAKE)
    if os.path.exists(top_cmake):
        files.append(top_cmake)

    return files


def replace_in_file(filepath: str, replacements: list[tuple[str, str]]) -> bool:
    with open(filepath, "r") as f:
        content = f.read()

    original = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content == original:
        return False

    with open(filepath, "w") as f:
        f.write(content)
    return True


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    old_name = sys.argv[1]
    new_name = sys.argv[2]

    validate_name(old_name, "old name")
    validate_name(new_name, "new name")

    if old_name == new_name:
        print("Error: old and new names are the same.")
        sys.exit(1)

    old_init = f"{old_name}_init"
    new_init = f"{new_name}_init"

    print(f"Renaming extension: {old_name} -> {new_name}")
    print(f"Init function: {old_init} -> {new_init}")
    print()

    # Order matters: replace the longer init name first to avoid partial matches
    replacements = [
        (old_init, new_init),
        (old_name, new_name),
    ]

    files = find_files()
    updated = []
    for filepath in files:
        if replace_in_file(filepath, replacements):
            rel = os.path.relpath(filepath, PROJECT_ROOT)
            updated.append(rel)
            print(f"  Updated {rel}")

    # Rename the .gdextension file and remove stale .uid
    old_gdext = os.path.join(PROJECT_ROOT, "godot", "project", f"{old_name}.gdextension")
    new_gdext = os.path.join(PROJECT_ROOT, "godot", "project", f"{new_name}.gdextension")
    old_uid = old_gdext + ".uid"
    if os.path.exists(old_gdext):
        os.rename(old_gdext, new_gdext)
        print(f"  Renamed {old_name}.gdextension -> {new_name}.gdextension")
    if os.path.exists(old_uid):
        os.remove(old_uid)
        print(f"  Removed {old_name}.gdextension.uid (Godot will regenerate it)")

    if not updated and not os.path.exists(new_gdext):
        print(f"  No references to '{old_name}' found. Is the name correct?")
        sys.exit(1)

    print()
    print("Done. Remember to re-run cmake to pick up the changes:")
    print("  cmake --preset debug")
    print("  cmake --build --preset debug")


if __name__ == "__main__":
    main()
