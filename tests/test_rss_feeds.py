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


class TestRSSFeeds:
    """Test suite for RSS feed functionality."""

    def test_main_feed_exists_and_linked(self, hugo_site, parse_html_fixture):
        """Test that main RSS feed exists and is properly linked on homepage."""
        # Check HTML link tag on homepage
        homepage = parse_html_fixture(hugo_site / "index.html")

        # Should have main feed link
        main_feed_link = homepage.find(
            "link",
            {"rel": "alternate", "type": "application/rss+xml", "href": "/feed.xml"},
        )
        assert main_feed_link is not None, "Homepage should have main RSS feed link"

        # Check title attribute
        title = main_feed_link.get("title", "")
        assert (
            "All Feed" in title or "Feed" in title
        ), f"Feed title should be descriptive, got: {title}"

        # Check actual feed file exists
        feed_file = hugo_site / "feed.xml"
        assert feed_file.exists(), "Main RSS feed file should exist at /feed.xml"

        # Feed should be valid XML
        self._validate_rss_structure(feed_file)

    def test_blog_section_feed_exists_and_linked(self, hugo_site, parse_html_fixture):
        """Test that blog section RSS feed exists and is properly linked."""
        # Check HTML link tag on homepage and blog index
        homepage = parse_html_fixture(hugo_site / "index.html")

        # Should have blog feed link
        blog_feed_link = homepage.find(
            "link",
            {"rel": "alternate", "type": "application/rss+xml"},
            href=lambda x: x and "blog/feed.xml" in x,
        )
        assert blog_feed_link is not None, "Homepage should have blog RSS feed link"

        # Check title attribute
        title = blog_feed_link.get("title", "")
        assert (
            "Blog Feed" in title
        ), f"Blog feed title should mention 'Blog', got: {title}"

        # Check actual feed file exists
        blog_feed_file = hugo_site / "blog" / "feed.xml"
        assert (
            blog_feed_file.exists()
        ), "Blog RSS feed file should exist at /blog/feed.xml"

        # Feed should be valid XML
        self._validate_rss_structure(blog_feed_file)

        # Also check on blog section page
        blog_index = hugo_site / "blog" / "index.html"
        if blog_index.exists():
            blog_page = parse_html_fixture(blog_index)
            blog_feed_link_on_blog = blog_page.find(
                "link",
                {"rel": "alternate", "type": "application/rss+xml"},
                href=lambda x: x and "blog/feed.xml" in x,
            )
            assert (
                blog_feed_link_on_blog is not None
            ), "Blog section page should have blog RSS feed link"

    def test_tag_specific_feeds_only_on_tag_pages(self, hugo_site, parse_html_fixture):
        """Test that tag-specific feeds only appear on their respective tag pages."""
        # Check homepage does NOT have tag-specific feed links
        homepage = parse_html_fixture(hugo_site / "index.html")

        # Look for any tag-specific feed links on homepage
        all_feed_links = homepage.find_all(
            "link", {"rel": "alternate", "type": "application/rss+xml"}
        )

        tag_feed_links = [
            link
            for link in all_feed_links
            if link.get("href", "").startswith("/tags/")
            and link.get("href", "").endswith("/feed.xml")
        ]

        assert (
            len(tag_feed_links) == 0
        ), f"Homepage should not have tag-specific feed links, found: {[link.get('href') for link in tag_feed_links]}"

        # Check that tag pages DO have their specific feed links
        thinking_tag_page = hugo_site / "tags" / "thinking-out-loud" / "index.html"
        if thinking_tag_page.exists():
            tag_page = parse_html_fixture(thinking_tag_page)

            # Should have its own tag feed
            tag_feed_link = tag_page.find(
                "link",
                {
                    "rel": "alternate",
                    "type": "application/rss+xml",
                    "href": "/tags/thinking-out-loud/feed.xml",
                },
            )
            assert (
                tag_feed_link is not None
            ), "Tag page should have its own RSS feed link"

            # Check title mentions the tag
            title = tag_feed_link.get("title", "")
            assert (
                "Thinking-Out-Loud" in title or "thinking-out-loud" in title.lower()
            ), f"Tag feed title should mention tag name, got: {title}"

            # Check actual feed file exists
            tag_feed_file = hugo_site / "tags" / "thinking-out-loud" / "feed.xml"
            assert tag_feed_file.exists(), "Tag RSS feed file should exist"

            # Feed should be valid XML
            self._validate_rss_structure(tag_feed_file)

    def test_feed_xml_structure_validation(self, hugo_site):
        """Test that RSS feeds have proper XML structure with required elements."""
        feed_paths = [hugo_site / "feed.xml", hugo_site / "blog" / "feed.xml"]

        # Add tag feeds if they exist
        tag_feed_file = hugo_site / "tags" / "thinking-out-loud" / "feed.xml"
        if tag_feed_file.exists():
            feed_paths.append(tag_feed_file)

        for feed_path in feed_paths:
            if feed_path.exists():
                self._validate_rss_structure(feed_path)

    def test_feed_content_has_items(self, hugo_site):
        """Test that RSS feeds contain actual content items."""
        # Main feed should have items
        main_feed = hugo_site / "feed.xml"
        assert main_feed.exists(), "Main feed should exist"

        with open(main_feed, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "xml")

        # Should have channel
        channel = soup.find("channel")
        assert channel is not None, "RSS feed should have channel element"

        # Should have items
        items = soup.find_all("item")
        assert len(items) > 0, "RSS feed should contain at least one item"

        # Check first item has required elements
        first_item = items[0]
        assert first_item.find("title") is not None, "RSS item should have title"
        assert first_item.find("link") is not None, "RSS item should have link"
        assert (
            first_item.find("description") is not None
        ), "RSS item should have description"

        # Check dates if present
        pub_date = first_item.find("pubDate")
        if pub_date and pub_date.string:
            # Should be a valid date format (basic check)
            assert (
                len(pub_date.string.strip()) > 10
            ), "pubDate should be properly formatted"

    def test_feed_links_are_absolute_urls(self, hugo_site, parse_html_fixture):
        """Test that RSS feed links use absolute URLs."""
        # Check homepage feed links
        homepage = parse_html_fixture(hugo_site / "index.html")

        feed_links = homepage.find_all(
            "link", {"rel": "alternate", "type": "application/rss+xml"}
        )

        assert len(feed_links) > 0, "Should have at least one RSS feed link"

        for link in feed_links:
            href = link.get("href", "")
            # RSS feed links should either be absolute URLs or root-relative paths
            assert href.startswith("http") or href.startswith(
                "/"
            ), f"RSS feed link should be absolute or root-relative, got: {href}"

    def test_all_tag_pages_have_consistent_feed_links(
        self, hugo_site, parse_html_fixture
    ):
        """Test that all tag pages have consistent feed link patterns."""
        tags_dir = hugo_site / "tags"
        if not tags_dir.exists():
            pytest.skip("No tags directory found")

        tag_pages_checked = 0

        for tag_dir in tags_dir.iterdir():
            if tag_dir.is_dir() and tag_dir.name != "page":
                index_file = tag_dir / "index.html"
                if index_file.exists():
                    tag_page = parse_html_fixture(index_file)
                    tag_name = tag_dir.name

                    # Should have main feed link
                    main_feed_link = tag_page.find(
                        "link",
                        {
                            "rel": "alternate",
                            "type": "application/rss+xml",
                            "href": "/feed.xml",
                        },
                    )
                    assert (
                        main_feed_link is not None
                    ), f"Tag page {tag_name} should have main feed link"

                    # Should have blog feed link
                    blog_feed_link = tag_page.find(
                        "link",
                        {"rel": "alternate", "type": "application/rss+xml"},
                        href=lambda x: x and "blog/feed.xml" in x,
                    )
                    assert (
                        blog_feed_link is not None
                    ), f"Tag page {tag_name} should have blog feed link"

                    # Should have its own tag feed link
                    tag_feed_href = f"/tags/{tag_name}/feed.xml"
                    tag_feed_link = tag_page.find(
                        "link",
                        {
                            "rel": "alternate",
                            "type": "application/rss+xml",
                            "href": tag_feed_href,
                        },
                    )
                    assert (
                        tag_feed_link is not None
                    ), f"Tag page {tag_name} should have its own feed link"

                    # Check that the feed file actually exists
                    tag_feed_file = tag_dir / "feed.xml"
                    assert (
                        tag_feed_file.exists()
                    ), f"Tag feed file should exist for {tag_name}"

                    tag_pages_checked += 1

                    # Only check first 3 tag pages to keep tests fast
                    if tag_pages_checked >= 3:
                        break

        assert tag_pages_checked > 0, "Should have checked at least one tag page"

    def test_feed_xml_encoding_and_namespace(self, hugo_site):
        """Test that RSS feeds have proper XML encoding and namespaces."""
        main_feed = hugo_site / "feed.xml"
        assert main_feed.exists(), "Main feed should exist"

        with open(main_feed, "r", encoding="utf-8") as f:
            content = f.read()

        # Should start with XML declaration
        assert content.startswith("<?xml"), "RSS feed should start with XML declaration"
        assert 'encoding="utf-8"' in content, "RSS feed should declare UTF-8 encoding"

        # Should have RSS namespace
        assert (
            'xmlns:atom="http://www.w3.org/2005/Atom"' in content
        ), "RSS feed should include Atom namespace"

        # Should be RSS 2.0
        assert 'version="2.0"' in content, "RSS feed should be version 2.0"

    def test_feed_has_required_channel_elements(self, hugo_site):
        """Test that RSS feeds have all required channel elements."""
        main_feed = hugo_site / "feed.xml"
        assert main_feed.exists(), "Main feed should exist"

        with open(main_feed, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "xml")
        channel = soup.find("channel")
        assert channel is not None, "RSS feed should have channel element"

        # Required channel elements
        required_elements = ["title", "link", "description"]
        for element in required_elements:
            elem = channel.find(element)
            assert elem is not None, f"RSS channel should have {element} element"
            assert (
                elem.string and len(elem.string.strip()) > 0
            ), f"RSS channel {element} should not be empty"

        # Check for Hugo generator
        generator = channel.find("generator")
        if generator and generator.string:
            assert "Hugo" in generator.string, "Generator should mention Hugo"

        # Check for atom:link self-reference
        atom_link = channel.find("atom:link", {"rel": "self"})
        if atom_link:
            href = atom_link.get("href", "")
            assert href.endswith("/feed.xml"), "Atom self-link should point to feed.xml"

    def test_blog_section_page_feed_links(self, hugo_site, parse_html_fixture):
        """Test that blog section index page has appropriate feed links."""
        blog_index = hugo_site / "blog" / "index.html"
        if not blog_index.exists():
            pytest.skip("Blog section index page not found")

        blog_page = parse_html_fixture(blog_index)

        # Should have main site feed
        main_feed_link = blog_page.find(
            "link",
            {"rel": "alternate", "type": "application/rss+xml", "href": "/feed.xml"},
        )
        assert main_feed_link is not None, "Blog section should have main feed link"

        # Should have blog-specific feed
        blog_feed_link = blog_page.find(
            "link",
            {"rel": "alternate", "type": "application/rss+xml"},
            href=lambda x: x and "blog/feed.xml" in x,
        )
        assert (
            blog_feed_link is not None
        ), "Blog section should have blog-specific feed link"

        # Should NOT have tag-specific feeds
        all_feed_links = blog_page.find_all(
            "link", {"rel": "alternate", "type": "application/rss+xml"}
        )

        tag_feeds = [
            link
            for link in all_feed_links
            if link.get("href", "").startswith("/tags/")
            and "/feed.xml" in link.get("href", "")
        ]

        assert (
            len(tag_feeds) == 0
        ), "Blog section should not have tag-specific feed links"

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
