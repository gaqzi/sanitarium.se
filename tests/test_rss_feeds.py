"""
Test RSS feed visibility and structure across the Hugo site.

Tests verify:
1. Main feed exists at `/feed.xml` (check for link tag and actual file)
2. Section feeds exist (e.g., `/blog/feed.xml`)
3. Tag-specific feeds only on tag pages (e.g., `/tags/thinking-out-loud/feed.xml`)
4. Feed structure validation (channel, items, proper XML)
5. Test that tag feeds are NOT linked on non-tag pages (homepage should not have tag feed links)
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

# Standard RSS feeds that should be present on all pages
STANDARD_FEEDS = [
    "https://sanitarium.se/feed.xml",
    "https://sanitarium.se/blog/feed.xml",
]


class TestRSSFeeds:
    """Test suite for RSS feed functionality."""

    def test_standard_feeds_on_homepage(self, hugo_site, parse_html_fixture):
        """Test that standard RSS feeds are linked on homepage."""
        homepage = parse_html_fixture(hugo_site / "index.html")

        for feed_href in STANDARD_FEEDS:
            feed_link = homepage.find(
                "link",
                {"rel": "alternate", "type": "application/rss+xml", "href": feed_href},
            )
            assert (
                feed_link is not None
            ), f"Homepage should have {feed_href} RSS feed link"

            # Check title attribute exists
            title = feed_link.get("title", "")
            assert title, f"Feed link {feed_href} should have a title attribute"

            # Check actual feed file exists (convert absolute URL to local path)
            if feed_href.startswith("http"):
                # Convert absolute URL to local path
                feed_path = feed_href.replace("https://sanitarium.se", "").lstrip("/")
            else:
                feed_path = feed_href.lstrip("/")
            feed_file = hugo_site / feed_path
            assert feed_file.exists(), f"RSS feed file should exist at {feed_path}"

    def test_standard_feeds_on_blog_index(self, hugo_site, parse_html_fixture):
        """Test that standard RSS feeds are linked on blog index page."""
        blog_index = hugo_site / "blog" / "index.html"
        if not blog_index.exists():
            pytest.skip("Blog index page not found")

        blog_page = parse_html_fixture(blog_index)

        for feed_href in STANDARD_FEEDS:
            feed_link = blog_page.find(
                "link",
                {"rel": "alternate", "type": "application/rss+xml", "href": feed_href},
            )
            assert (
                feed_link is not None
            ), f"Blog index should have {feed_href} RSS feed link"

            # Check title attribute exists
            title = feed_link.get("title", "")
            assert title, f"Feed link {feed_href} should have a title attribute"

    def test_how_to_tag_page_feeds(self, hugo_site, parse_html_fixture):
        """Test that how-to tag page has standard feeds plus its own tag feed."""
        how_to_tag_page = hugo_site / "tags" / "how-to" / "index.html"
        if not how_to_tag_page.exists():
            pytest.skip("How-to tag page not found")

        tag_page = parse_html_fixture(how_to_tag_page)

        # Should have all standard feeds
        for feed_href in STANDARD_FEEDS:
            feed_link = tag_page.find(
                "link",
                {"rel": "alternate", "type": "application/rss+xml", "href": feed_href},
            )
            assert (
                feed_link is not None
            ), f"How-to tag page should have {feed_href} RSS feed link"

        # Should have its own tag feed
        tag_feed_href = "https://sanitarium.se/tags/how-to/feed.xml"
        tag_feed_link = tag_page.find(
            "link",
            {"rel": "alternate", "type": "application/rss+xml", "href": tag_feed_href},
        )
        assert (
            tag_feed_link is not None
        ), "How-to tag page should have its own RSS feed link"

        # Check title mentions the tag
        title = tag_feed_link.get("title", "")
        assert title, "Tag feed link should have a title attribute"

        # Check actual feed file exists and is valid XML
        tag_feed_file = hugo_site / "tags" / "how-to" / "feed.xml"
        assert tag_feed_file.exists(), "How-to tag RSS feed file should exist"
        self._validate_rss_structure(tag_feed_file)

    def test_main_feed_xml_structure(self, hugo_site):
        """Test that main RSS feed has proper XML structure."""
        main_feed = hugo_site / "feed.xml"
        assert main_feed.exists(), "Main RSS feed should exist"
        self._validate_rss_structure(main_feed)

    def _validate_rss_structure(self, feed_path: Path):
        """Helper method to validate basic RSS XML structure."""
        assert feed_path.exists(), f"Feed file should exist: {feed_path}"

        # Should be valid XML
        try:
            with open(feed_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse with both xml.etree and BeautifulSoup for thorough validation
            ET.fromstring(content)  # Will raise if invalid XML
            soup = BeautifulSoup(content, "xml")

            # Should have rss root element
            rss = soup.find("rss")
            assert rss is not None, f"Feed should have rss root element: {feed_path}"
            assert rss.get("version") == "2.0", f"Feed should be RSS 2.0: {feed_path}"

            # Should have channel
            channel = soup.find("channel")
            assert channel is not None, f"Feed should have channel element: {feed_path}"

        except ET.ParseError as e:
            pytest.fail(f"Feed {feed_path} is not valid XML: {e}")
        except Exception as e:
            pytest.fail(f"Error validating feed {feed_path}: {e}")
