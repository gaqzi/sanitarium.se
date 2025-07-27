"""
Test JSON-LD structured data across the Hugo site.

Tests verify:
1. WebSite schema on homepage with required fields
2. BlogPosting schema on individual posts with required fields
3. Required fields: headline, author, datePublished
4. JSON-LD validity and proper schema.org types
5. Author, publisher, and metadata field validation
"""

import json
from datetime import datetime
from pathlib import Path

import pytest
from bs4 import BeautifulSoup


class TestStructuredData:
    """Test suite for JSON-LD structured data functionality."""

    def _extract_json_ld_scripts(self, soup):
        """Extract and validate JSON-LD script tags from soup."""
        json_ld_scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        assert len(json_ld_scripts) > 0, "Page should have JSON-LD structured data"
        return json_ld_scripts

    def _get_schema_by_type(self, soup, schema_type):
        """Get schema of specific @type from page, with JSON validation."""
        json_ld_scripts = self._extract_json_ld_scripts(soup)

        for script in json_ld_scripts:
            if script.string:
                try:
                    data = json.loads(script.string.strip())
                    if data.get("@type") == schema_type:
                        return data
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON-LD structure: {e}")

        return None

    def _validate_schema_context(self, schema):
        """Validate schema uses correct schema.org context."""
        assert (
            schema.get("@context") == "https://schema.org"
        ), "Should use schema.org context"

    def _validate_person_author(self, author):
        """Validate Person schema structure for author."""
        assert author.get("@type") == "Person", "Author should be a Person"
        assert "name" in author, "Author should have name"
        assert len(author["name"].strip()) > 0, "Author name should not be empty"

    def _validate_absolute_url(self, url, field_name="URL"):
        """Validate URL is absolute (starts with http)."""
        assert url.startswith("http"), f"{field_name} should be absolute"

    def _validate_iso_date(self, date_string, field_name):
        """Validate date string is valid ISO 8601 format."""
        try:
            return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(f"{field_name} should be valid ISO 8601 format: {date_string}")

    def _get_and_validate_schema(self, soup, schema_type):
        """Get schema and validate basic structure (context and type)."""
        schema = self._get_schema_by_type(soup, schema_type)
        assert schema is not None, f"Page should have {schema_type} schema"

        self._validate_schema_context(schema)
        assert schema.get("@type") == schema_type, f"Should have {schema_type} type"

        return schema

    def _validate_content_metadata(self, schema):
        """Validate common content metadata (url, name/headline, description)."""
        assert "url" in schema, "Schema should have url property"
        self._validate_absolute_url(schema["url"])

        # Handle both 'name' (WebSite) and 'headline' (BlogPosting)
        title_field = "name" if "name" in schema else "headline"
        assert title_field in schema, f"Schema should have {title_field} property"
        assert (
            len(schema[title_field].strip()) > 0
        ), f"{title_field.title()} should not be empty"

        assert "description" in schema, "Schema should have description property"
        assert len(schema["description"].strip()) > 0, "Description should not be empty"

    def _validate_author_structure(self, schema):
        """Validate author structure, handling both single and multiple authors."""
        assert "author" in schema, "Schema should have author property"

        authors = schema["author"]
        if isinstance(authors, list):
            assert len(authors) > 0, "Should have at least one author"
            for author in authors:
                self._validate_person_author(author)
        else:
            self._validate_person_author(authors)

    def _get_blog_posting_schema(self, get_post_html_fixture):
        """Get BlogPosting schema from the test post."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        return self._get_and_validate_schema(soup, "BlogPosting")

    def test_homepage_website_schema(self, hugo_site, parse_html_fixture):
        """Test that homepage has valid WebSite schema with required fields."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        website_schema = self._get_and_validate_schema(homepage, "WebSite")

        self._validate_content_metadata(website_schema)
        self._validate_author_structure(website_schema)

        # Validate potential action (search)
        if "potentialAction" in website_schema:
            action = website_schema["potentialAction"]
            assert (
                action.get("@type") == "SearchAction"
            ), "potentialAction should be SearchAction"
            assert "target" in action, "SearchAction should have target"
            assert "query-input" in action, "SearchAction should have query-input"

    def test_individual_post_blog_posting_schema(
        self, hugo_site, get_post_html_fixture
    ):
        """Test that individual posts have valid BlogPosting schema with required fields."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        blog_posting_schema = self._get_and_validate_schema(soup, "BlogPosting")

        self._validate_content_metadata(blog_posting_schema)
        self._validate_author_structure(blog_posting_schema)

        # Validate post-specific content
        headline = blog_posting_schema["headline"]
        assert "hat" in headline.lower(), "Headline should relate to post content"

        assert (
            "which-hat-are-you-wearing" in blog_posting_schema["url"]
        ), "URL should include post slug"

        assert (
            "datePublished" in blog_posting_schema
        ), "BlogPosting should have datePublished"
        self._validate_iso_date(blog_posting_schema["datePublished"], "datePublished")

    def test_blog_posting_publisher_information(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes proper publisher information."""
        blog_posting_schema = self._get_blog_posting_schema(get_post_html_fixture)

        # Validate publisher information
        assert "publisher" in blog_posting_schema, "BlogPosting should have publisher"
        publisher = blog_posting_schema["publisher"]
        assert (
            publisher.get("@type") == "Organization"
        ), "Publisher should be an Organization"
        assert "name" in publisher, "Publisher should have name"
        assert len(publisher["name"].strip()) > 0, "Publisher name should not be empty"

        # Validate publisher logo
        if "logo" in publisher:
            logo = publisher["logo"]
            assert (
                logo.get("@type") == "ImageObject"
            ), "Publisher logo should be ImageObject"
            assert "url" in logo, "Logo should have url"
            self._validate_absolute_url(logo["url"], "Logo URL")

    def test_blog_posting_main_entity_of_page(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes mainEntityOfPage property."""
        blog_posting_schema = self._get_blog_posting_schema(get_post_html_fixture)

        # Validate mainEntityOfPage
        assert (
            "mainEntityOfPage" in blog_posting_schema
        ), "BlogPosting should have mainEntityOfPage"
        main_entity = blog_posting_schema["mainEntityOfPage"]
        assert (
            main_entity.get("@type") == "WebPage"
        ), "mainEntityOfPage should be WebPage"
        assert "@id" in main_entity, "WebPage should have @id"
        self._validate_absolute_url(main_entity["@id"], "WebPage @id")

    def test_blog_posting_date_fields(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes proper date fields."""
        blog_posting_schema = self._get_blog_posting_schema(get_post_html_fixture)

        # Validate datePublished (required)
        assert (
            "datePublished" in blog_posting_schema
        ), "BlogPosting should have datePublished"
        pub_date = self._validate_iso_date(
            blog_posting_schema["datePublished"], "datePublished"
        )

        # Validate dateModified (should be present)
        assert (
            "dateModified" in blog_posting_schema
        ), "BlogPosting should have dateModified"
        mod_date = self._validate_iso_date(
            blog_posting_schema["dateModified"], "dateModified"
        )

        # dateModified should be >= datePublished
        assert mod_date >= pub_date, "dateModified should be >= datePublished"

    def test_blog_posting_word_count(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes wordCount property."""
        blog_posting_schema = self._get_blog_posting_schema(get_post_html_fixture)

        # Validate wordCount
        if "wordCount" in blog_posting_schema:
            word_count = blog_posting_schema["wordCount"]
            # Should be a number or string representation of a number
            try:
                count = int(word_count)
                assert count > 0, "Word count should be positive"
                assert count > 100, "Post should have substantial word count"
            except (ValueError, TypeError):
                pytest.fail(f"wordCount should be numeric: {word_count}")

    def test_json_ld_valid_json_syntax(
        self, hugo_site, get_post_html_fixture, parse_html_fixture
    ):
        """Test that all JSON-LD on site has valid JSON syntax."""
        # Test homepage
        homepage = parse_html_fixture(hugo_site / "index.html")
        self._extract_json_ld_scripts(homepage)  # This validates JSON syntax

        # Test individual post
        post_soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        self._extract_json_ld_scripts(post_soup)  # This validates JSON syntax

    def test_schema_org_context_consistency(
        self, hugo_site, get_post_html_fixture, parse_html_fixture
    ):
        """Test that all JSON-LD uses consistent schema.org context."""
        # Test homepage
        homepage = parse_html_fixture(hugo_site / "index.html")
        json_ld_scripts = self._extract_json_ld_scripts(homepage)
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                self._validate_schema_context(data)

        # Test individual post
        post_soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        json_ld_scripts = self._extract_json_ld_scripts(post_soup)
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                self._validate_schema_context(data)

    def test_blog_posting_image_handling(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema handles image property correctly."""
        blog_posting_schema = self._get_blog_posting_schema(get_post_html_fixture)

        # If image is present, validate it
        if "image" in blog_posting_schema:
            image = blog_posting_schema["image"]
            assert isinstance(image, str), "Image should be a URL string"
            self._validate_absolute_url(image, "Image")

    def test_multiple_authors_handling(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema handles multiple authors correctly."""
        blog_posting_schema = self._get_blog_posting_schema(get_post_html_fixture)

        self._validate_author_structure(blog_posting_schema)

        # Validate authors are in list format (test-specific assertion)
        authors = blog_posting_schema["author"]
        assert isinstance(authors, list), "Authors should be in list format"
