"""
Shared fixtures and helper functions for pytest tests.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope="session")
def hugo_site():
    """Build the Hugo site once per test session and return the output directory."""
    # Get the project root (parent of tests directory)
    project_root = Path(__file__).parent.parent

    # Create a temporary directory for the built site
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "public"

        # Build the site using Hugo
        result = subprocess.run(
            ["hugo", "--destination", str(output_dir)],
            cwd=project_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Hugo build failed: {result.stderr}")

        yield output_dir


def build_site() -> Path:
    """Build Hugo site in temp directory and return the path."""
    # Get the project root (parent of tests directory)
    project_root = Path(__file__).parent.parent

    # Create a temporary directory for the built site
    temp_dir = tempfile.mkdtemp()
    output_dir = Path(temp_dir) / "public"

    # Build the site using Hugo
    result = subprocess.run(
        ["hugo", "--destination", str(output_dir)],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Hugo build failed: {result.stderr}")

    return output_dir


def parse_html(path: Path) -> BeautifulSoup:
    """Parse HTML file with BeautifulSoup."""
    if not path.exists():
        raise FileNotFoundError(f"HTML file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return BeautifulSoup(content, "lxml")


def get_post_html(hugo_site: Path, slug: str) -> BeautifulSoup:
    """Get parsed HTML for a specific post."""
    # Handle different slug formats
    if slug.startswith("/"):
        slug = slug[1:]
    if slug.endswith("/"):
        slug = slug[:-1]

    # Try common post paths
    possible_paths = [
        hugo_site / f"{slug}/index.html",
        hugo_site / f"{slug}.html",
        hugo_site / f"blog/{slug}/index.html",
        hugo_site / f"blog/{slug}.html",
    ]

    for path in possible_paths:
        if path.exists():
            return parse_html(path)

    raise FileNotFoundError(f"Post not found: {slug}")


def get_meta_content(soup: BeautifulSoup, name: str) -> Optional[str]:
    """Extract meta tag content by name attribute."""
    meta_tag = soup.find("meta", attrs={"name": name})
    if meta_tag:
        return meta_tag.get("content")
    return None


def get_og_content(soup: BeautifulSoup, property: str) -> Optional[str]:
    """Extract Open Graph content by property attribute."""
    og_tag = soup.find("meta", attrs={"property": f"og:{property}"})
    if og_tag:
        return og_tag.get("content")
    return None


# Additional helper functions for common test patterns
def get_twitter_content(soup: BeautifulSoup, name: str) -> Optional[str]:
    """Extract Twitter Card content by name attribute."""
    twitter_tag = soup.find("meta", attrs={"name": f"twitter:{name}"})
    if twitter_tag:
        return twitter_tag.get("content")
    return None


def get_json_ld(soup: BeautifulSoup) -> Optional[dict]:
    """Extract and parse JSON-LD structured data."""
    import json

    script_tag = soup.find("script", attrs={"type": "application/ld+json"})
    if script_tag and script_tag.string:
        try:
            return json.loads(script_tag.string)
        except json.JSONDecodeError:
            return None
    return None


def get_rss_feed(hugo_site: Path, feed_path: str) -> BeautifulSoup:
    """Parse RSS feed XML."""
    if not feed_path.startswith("/"):
        feed_path = "/" + feed_path

    feed_file = hugo_site / feed_path.lstrip("/")
    if not feed_file.exists():
        raise FileNotFoundError(f"RSS feed not found: {feed_path}")

    with open(feed_file, "r", encoding="utf-8") as f:
        content = f.read()

    return BeautifulSoup(content, "xml")


def get_all_posts(hugo_site: Path) -> list[Path]:
    """Get all blog post HTML files."""
    blog_dir = hugo_site / "blog"
    if not blog_dir.exists():
        return []

    posts = []
    for year_dir in blog_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit():
            for month_dir in year_dir.iterdir():
                if month_dir.is_dir() and month_dir.name.isdigit():
                    for day_dir in month_dir.iterdir():
                        if day_dir.is_dir() and day_dir.name.isdigit():
                            for post_dir in day_dir.iterdir():
                                if post_dir.is_dir():
                                    index_file = post_dir / "index.html"
                                    if index_file.exists():
                                        posts.append(index_file)

    return posts


def has_class(element, class_name: str) -> bool:
    """Check if an element has a specific CSS class."""
    if element and element.get("class"):
        return class_name in element.get("class")
    return False


@pytest.fixture
def get_post_html_fixture(hugo_site):
    """Fixture that returns the get_post_html function with hugo_site bound."""

    def _get_post_html(slug: str) -> BeautifulSoup:
        return get_post_html(hugo_site, slug)

    return _get_post_html


@pytest.fixture
def parse_html_fixture():
    """Fixture that returns the parse_html function."""
    return parse_html


@pytest.fixture
def get_all_posts_fixture(hugo_site):
    """Fixture that returns the get_all_posts function with hugo_site bound."""

    def _get_all_posts() -> list[Path]:
        return get_all_posts(hugo_site)

    return _get_all_posts


@pytest.fixture
def has_class_fixture():
    """Fixture that returns the has_class function."""
    return has_class
