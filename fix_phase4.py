#!/usr/bin/env python3
"""Fix the app_main.py by removing duplicate Phase 4 section."""

with open('app_main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove the old Phase 4 section (lines 1970-2209)
# Keep everything before line 1970 and everything from line 2210 onwards

new_lines = lines[:1969] + lines[2209:]

with open('app_main.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"✓ Removed old Phase 4 section")
print(f"  Original: {len(lines)} lines")
print(f"  New: {len(new_lines)} lines")
print(f"  Removed: {len(lines) - len(new_lines)} lines")
