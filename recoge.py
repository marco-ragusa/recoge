#!/usr/bin/env python3

import os
import sys
import xml.sax.saxutils as saxutils


def escape_xml(text):
    """Escape special characters for XML."""
    return saxutils.escape(text)


def generate_tree(directory, prefix=""):
    """Generate a text-based tree structure."""
    entries = os.listdir(directory)
    entries.sort()  # Sort entries for consistency
    tree_lines = []

    for index, entry in enumerate(entries):
        entry_path = os.path.join(directory, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "

        if os.path.isdir(entry_path):
            tree_lines.append(f"{prefix}{connector}{entry}/")
            tree_lines.extend(generate_tree(entry_path, prefix + ("    " if index == len(entries) - 1 else "│   ")))
        else:
            tree_lines.append(f"{prefix}{connector}{entry}")

    return tree_lines


def generate_tree_xml(directory, indent=2):
    """Generate the XML structure for the directory."""
    indent_space = "  " * indent
    dir_name = os.path.basename(directory)
    yield f'{indent_space}<directory name="{escape_xml(dir_name)}">'

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            yield from generate_tree_xml(item_path, indent + 1)
        elif os.path.isfile(item_path):
            yield f'{indent_space}  <file name="{escape_xml(item)}">'
            yield f'{indent_space}    <content>'
            try:
                with open(item_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        yield f'{indent_space}      {escape_xml(line.strip())}'
            except Exception as e:
                yield f'{indent_space}      <!-- Error reading file: {e} -->'
            yield f'{indent_space}    </content>'
            yield f'{indent_space}  </file>'

    yield f'{indent_space}</directory>'


def main():
    if len(sys.argv) < 2:
        print("Usage: python recoge.py <directory> [output_file]")
        sys.exit(1)

    base_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.xml"

    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' does not exist!")
        sys.exit(2)

    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("<context>\n")

        # Generate pretty tree structure
        output.write("  <tree><![CDATA[\n")
        for line in generate_tree(base_dir):
            output.write(line + "\n")
        output.write("  ]]></tree>\n")

        # Generate XML directory tree
        output.write("  <fileTree>\n")
        for line in generate_tree_xml(base_dir):
            output.write(line + "\n")
        output.write("  </fileTree>\n")

        output.write("</context>\n")

    print(f"XML output saved to {output_file}")


if __name__ == "__main__":
    main()
