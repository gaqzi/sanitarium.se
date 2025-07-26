#!/usr/bin/env python3
"""
Blog Tag Collector

Collects all tags from markdown files in the content/ directory
and outputs a YAML document with tag counts sorted alphabetically.
"""

import argparse
import glob
import os
import re
import sys
from collections import defaultdict


def extract_front_matter(content):
    """Extract YAML front matter from markdown content."""
    if not content.startswith("---"):
        return None

    try:
        # Find the end of front matter
        end_delimiter = content.find("---", 3)
        if end_delimiter == -1:
            return None

        front_matter = content[3:end_delimiter].strip()
        return parse_simple_yaml(front_matter)
    except Exception:
        return None


def parse_simple_yaml(yaml_text):
    """Simple YAML parser for front matter (tags only)."""
    result = {}
    lines = yaml_text.split("\n")
    current_key = None
    current_list = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Handle key: value pairs
        if ":" in line and not line.startswith("-"):
            if current_key == "tags" and current_list:
                result[current_key] = current_list
                current_list = []

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "tags":
                current_key = "tags"
                if value and value != "":
                    # Single tag on same line
                    if value.startswith("[") and value.endswith("]"):
                        # Handle [tag1, tag2] format
                        tags = [t.strip(" \"'") for t in value[1:-1].split(",")]
                        result["tags"] = [t for t in tags if t]
                    else:
                        # Single tag
                        result["tags"] = [value.strip(" \"'")]
                else:
                    current_list = []
            else:
                current_key = None
                result[key] = value.strip(" \"'")

        # Handle list items
        elif line.startswith("-") and current_key == "tags":
            item = line[1:].strip(" \"'")
            if item:
                current_list.append(item)

    # Don't forget the last list
    if current_key == "tags" and current_list:
        result[current_key] = current_list

    return result


def collect_tags_from_file(filepath):
    """Extract tags from a single markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_front_matter(content)
        if not front_matter or "tags" not in front_matter:
            return []

        tags = front_matter["tags"]
        if isinstance(tags, list):
            return [tag.strip() for tag in tags if tag and tag.strip()]
        elif isinstance(tags, str):
            # Handle case where tags might be a single string
            return [tags.strip()]
        else:
            return []

    except (IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return []


def collect_all_tags(content_dir="content"):
    """Collect tags from all markdown files in the content directory."""
    tag_counts = defaultdict(int)
    processed_files = 0

    # Find all markdown files recursively
    pattern = os.path.join(content_dir, "**", "*.md")
    markdown_files = glob.glob(pattern, recursive=True)

    print(f"Processing {len(markdown_files)} markdown files...", file=sys.stderr)

    for filepath in markdown_files:
        tags = collect_tags_from_file(filepath)
        for tag in tags:
            tag_counts[tag] += 1
        processed_files += 1

    print(
        f"Processed {processed_files} files, found {len(tag_counts)} unique tags",
        file=sys.stderr,
    )
    return tag_counts


def output_yaml(tag_counts, output_file=None):
    """Output tag counts as YAML in the requested format."""
    # Sort tags alphabetically
    sorted_tags = sorted(tag_counts.items())

    # Format as list of "tag: count" entries
    yaml_data = []
    for tag, count in sorted_tags:
        yaml_data.append(f"{tag}: {count}")

    output = "\n".join(f"- {entry}" for entry in yaml_data)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
            f.write("\n")
        print(f"Tag counts written to {output_file}", file=sys.stderr)
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Collect tags from blog markdown files"
    )
    parser.add_argument(
        "-d",
        "--directory",
        default="content",
        help="Content directory to scan (default: content)",
    )
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' not found", file=sys.stderr)
        sys.exit(1)

    tag_counts = collect_all_tags(args.directory)

    if not tag_counts:
        print("No tags found in any markdown files", file=sys.stderr)
        sys.exit(0)

    output_yaml(tag_counts, args.output)


if __name__ == "__main__":
    main()
