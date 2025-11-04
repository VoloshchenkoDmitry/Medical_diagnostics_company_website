#!/usr/bin/env python3
"""
Script to fix common PEP8 issues automatically
"""

import glob
import os


def fix_no_newline_at_end(file_path):
    """Add newline at end of file if missing"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if content and not content.endswith("\n"):
            with open(file_path, "a", encoding="utf-8") as f:
                f.write("\n")
            print(f"✓ Fixed: {file_path}")
            return True
    except Exception as e:
        print(f"✗ Error fixing {file_path}: {e}")
    return False


def main():
    """Main function to fix PEP8 issues"""
    files_to_fix = [
        "apps/appointments/tests/test_basic.py",
        "apps/common/tests/test_basic.py",
        "apps/common/tests/test_urls.py",
        "apps/services/tests/test_basic.py",
        "apps/services/tests/test_urls.py",
        "apps/users/tests/test_basic.py",
        "scripts/fix_pep8.py",
    ]

    fixed_count = 0
    for file_pattern in files_to_fix:
        for file_path in glob.glob(file_pattern, recursive=True):
            if fix_no_newline_at_end(file_path):
                fixed_count += 1

    print(f"\nFixed {fixed_count} files")

    # Run flake8 again to verify
    print("\nRunning flake8 verification...")
    os.system("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics")


if __name__ == "__main__":
    main()
