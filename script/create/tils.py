#!/usr/bin/env python
import argparse
import sys
from dataclasses import dataclass


def _generate_timestamp() -> str:
    """Generate RFC3339 formatted timestamp with local timezone"""
    from datetime import datetime

    # Use local timezone and RFC3339 format with microseconds
    # Microseconds ensure TILs are sorted in the order they were added
    dt = datetime.now().astimezone()
    timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    # Insert colon in timezone offset for RFC3339 compliance
    if len(timestamp) >= 5 and timestamp[-5] in "+-":
        timestamp = timestamp[:-2] + ":" + timestamp[-2:]

    return timestamp


def _clean_tag(tag_text: str) -> str:
    """Clean and normalize tag text"""
    import re

    # Convert to lowercase
    tag = tag_text.lower()
    # Replace spaces with hyphens
    tag = tag.replace(" ", "-")
    # Remove special characters, keep only letters, numbers, hyphens
    tag = re.sub(r"[^a-z0-9\-]", "", tag)
    return tag


def _is_til_start(line: str) -> bool:
    """Check if line starts a TIL entry"""
    stripped = line.strip()
    return any(
        stripped.startswith(prefix)
        for prefix in ["- TIL::", "- [[TIL]]:", "- [[TIL]]", "- TIL:"]
    )


def _extract_til_content(line: str) -> str:
    """Extract TIL content by removing the prefix"""
    if line.startswith("- TIL:: "):
        return line[8:]  # Remove "- TIL:: "
    elif line.startswith("- [[TIL]]: "):
        return line[11:]  # Remove "- [[TIL]]: "
    elif line.startswith("- [[TIL]] "):
        return line[10:]  # Remove "- [[TIL]] "
    elif line.startswith("- TIL: "):
        return line[7:]  # Remove "- TIL: "
    return ""


def _process_hashtags(
    text: str, extract_tags: bool = True, remove_from_body: bool = True
) -> tuple[set[str], str]:
    """
    Process hashtags in text, optionally extracting tags and/or removing them from body.

    Args:
        text: The text to process
        extract_tags: Whether to extract hashtags as tags (excluding those in markdown links)
        remove_from_body: Whether to remove hashtags from the returned text (excluding those in markdown links)

    Returns:
        tuple: (set of extracted tags, processed text)
    """
    import re

    hashtag_pattern = r"#([a-zA-Z0-9\-_]+)"
    markdown_link_pattern = r"\[([^\]]*)\]\(([^)]+)\)"
    extracted_tags = set()

    # Find all markdown links to exclude hashtags within them
    markdown_links = []
    for match in re.finditer(markdown_link_pattern, text):
        markdown_links.append((match.start(), match.end()))

    # Process hashtags
    hashtags_to_remove = []
    for match in re.finditer(hashtag_pattern, text):
        hashtag_start = match.start()
        hashtag_end = match.end()

        # Check if this hashtag is within a markdown link
        is_in_link = any(
            link_start <= hashtag_start < link_end
            for link_start, link_end in markdown_links
        )

        if not is_in_link:
            if extract_tags:
                tag = _clean_tag(match.group(1))
                if tag:  # Only add non-empty tags
                    extracted_tags.add(tag)

            if remove_from_body:
                hashtags_to_remove.append((hashtag_start, hashtag_end))

    # Remove hashtags from body in reverse order to maintain correct positions
    processed_text = text
    if remove_from_body:
        for start, end in sorted(hashtags_to_remove, reverse=True):
            processed_text = processed_text[:start] + processed_text[end:]

    return extracted_tags, processed_text


@dataclass
class TIL:
    body: str
    tags: list[str]

    def as_content(self, timestamp: str = None) -> str:
        """Generate full Hugo post content with front matter"""
        if timestamp is None:
            timestamp = _generate_timestamp()

        front_matter = self._generate_front_matter(timestamp)
        return front_matter + self.body

    def _generate_front_matter(self, timestamp: str) -> str:
        """Generate YAML front matter"""
        lines = [
            "---",
            "author: 'björn'",
            f"date: {timestamp}",
            f"daily: ['{timestamp.split('T')[0]}']",
            "lastmod: ''",
        ]

        if self.tags:
            lines.append("tags:")
            lines.extend(f"  - {tag}" for tag in self.tags)
        else:
            lines.append("tags: []")

        lines.append("---")
        return "\n".join(lines) + "\n"

    def filename(self, date: str = None) -> str:
        """Generate filename based on date and body content"""
        import re
        from datetime import datetime

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        if not self.body:
            return f"{date}-.md"

        # Convert to lowercase and remove apostrophes
        text = self.body.lower().replace("'", "")

        # Handle quoted content: remove anything in quotes and take what's left
        text = re.sub(r'["\'][^"\']*["\']', " ", text)

        # Stop at punctuation
        text = re.split(r"[.!?:…,]", text)[0]

        # Convert to slug: keep only letters, numbers, spaces; replace non-alphanumeric with hyphens
        text = re.sub(r"[^a-z0-9\s]", "-", text)

        # Split into words and take first few words
        words = [w for w in text.split() if w and w != "-"]
        slug = "-".join(words)

        # Clean up multiple hyphens and trim
        slug = re.sub(r"-+", "-", slug).strip("-")

        return f"{date}-{slug}.md"


def parse_til(input_text: str) -> TIL:
    """Parse TIL entry and return TIL object"""
    import re

    # Handle multi-line input
    lines = input_text.split("\n")
    first_line = lines[0].strip()

    text_content = _extract_til_content(first_line)

    # Add remaining lines, handling indentation
    if len(lines) > 1:
        additional_lines = []
        for line in lines[1:]:
            # Stop at next bullet point
            if line.strip().startswith("- "):
                break

            # For lines with content, remove 2-space indentation if present
            # For empty lines or lines with only spaces, preserve them as-is
            if line.strip() == "":  # Empty line or only spaces
                additional_lines.append(line)
            elif line.startswith("  "):
                additional_lines.append(line[2:])
            else:
                additional_lines.append(line)

        if additional_lines:
            text_content += "\n" + "\n".join(additional_lines)

    text = text_content

    # Extract tags from [[tag]] patterns (including nested ones like [text]([[tag]])) and hashtags
    tag_pattern = r"\[\[([^\]]+)\]\]"
    nested_pattern = r"\[([^\]]+)\]\(\[\[([^\]]+)\]\]\)"
    tags = set()

    # Handle nested patterns first: [text][[tag]] -> extract tag from second brackets
    for match in re.finditer(nested_pattern, text):
        tag = _clean_tag(match.group(2))
        if tag:  # Only add non-empty tags
            tags.add(tag)

    # Handle regular [[tag]] patterns
    for match in re.finditer(tag_pattern, text):
        # Skip if this is part of a nested pattern we already processed
        if not re.search(r"\[[^\]]+\]" + re.escape(match.group(0)), text):
            tag = _clean_tag(match.group(1))
            if tag:  # Only add non-empty tags
                tags.add(tag)

    # Handle hashtag patterns using unified helper function
    hashtag_tags, _ = _process_hashtags(text, extract_tags=True, remove_from_body=False)
    tags.update(hashtag_tags)

    # Remove patterns from body text
    # First remove nested patterns: [text]([[tag]]) -> text
    body = re.sub(nested_pattern, r"\1", text)
    # Then remove regular [[tag]] patterns: [[tag]] -> tag
    body = re.sub(tag_pattern, r"\1", body)
    # Then remove hashtags from body text using unified helper function
    _, body = _process_hashtags(body, extract_tags=False, remove_from_body=True)

    body = body.strip()

    # Capitalize first letter if body starts with lowercase
    if body and body[0].islower():
        body = body[0].upper() + body[1:]

    return TIL(body=body, tags=list(tags))


def parse_multiple_tils(input_text: str) -> list[TIL]:
    """Parse multiple TIL entries from input text and return list of TIL objects"""
    tils = []
    lines = input_text.split("\n")
    current_til_lines = []

    for line in lines:
        is_til_start = _is_til_start(line)

        if is_til_start:
            if current_til_lines:
                til_text = "\n".join(current_til_lines)
                tils.append(parse_til(til_text))

            current_til_lines = [line]
        else:
            if current_til_lines:
                current_til_lines.append(line)
    if current_til_lines:
        til_text = "\n".join(current_til_lines)
        tils.append(parse_til(til_text))

    return tils


def create_til_files(tils: list[TIL], output_dir: str = "content/til") -> None:
    """Create TIL files in the specified output directory"""
    from pathlib import Path

    til_dir = Path(output_dir)
    til_dir.mkdir(parents=True, exist_ok=True)
    for til in tils:
        filename = til.filename()
        filepath = til_dir / filename
        content = til.as_content()

        # Write file with trailing newline per CLAUDE.md
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content + "\n")


def main():
    """Main function to process TILs from STDIN and create files"""
    parser = argparse.ArgumentParser(
        description="Parse TIL entries from STDIN and create Hugo markdown files"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="content/til",
        help="Output directory for TIL files (default: content/til)",
    )

    args = parser.parse_args()

    try:
        input_text = sys.stdin.read().strip()
    except KeyboardInterrupt:
        print("Interrupted by user", file=sys.stderr)
        sys.exit(1)

    if not input_text:
        print("No input provided on STDIN", file=sys.stderr)
        sys.exit(0)

    try:
        tils = parse_multiple_tils(input_text)
    except Exception as e:
        print(f"Error parsing TILs: {e}", file=sys.stderr)
        sys.exit(1)

    if not tils:
        print("No valid TIL entries found in input", file=sys.stderr)
        sys.exit(0)

    try:
        create_til_files(tils, output_dir=args.output_dir)
        print(f"Created {len(tils)} TIL file(s) in {args.output_dir}", file=sys.stderr)

        for til in tils:
            filename = til.filename()
            print(f"  - {filename}", file=sys.stderr)

    except PermissionError as e:
        print(f"Permission error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error creating files: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
