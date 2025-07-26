"""
Test author display logic across the Hugo site.

Tests verify:
1. Author avatars are hidden in listing views (homepage, blog listing, tag pages) - hideAuthor: true
2. Author avatars show on individual posts - hideAuthor: false
3. Author metadata consistency across templates
4. Author avatar images exist and render correctly
5. Author links point to correct pages
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


class TestAuthorDisplay:
    """Test suite for author display functionality."""

    def test_individual_post_shows_author_avatar(
        self, hugo_site, get_post_html_fixture
    ):
        """Test that individual posts show author avatars (hideAuthor: false)."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        # Look for author avatar in meta section
        author_avatar = soup.find("img", class_="author-avatar")
        assert author_avatar is not None, "Individual post should display author avatar"

        # Verify avatar attributes - note the URL encoding of björn
        expected_src = "/img/authors/bj%c3%b6rn.jpg"  # URL-encoded björn
        assert (
            author_avatar.get("src") == expected_src
        ), f"Avatar src should be '{expected_src}' but was '{author_avatar.get('src')}'"
        assert (
            author_avatar.get("alt") == "Björn Andersson"
        ), f"Avatar alt should be 'Björn Andersson' but was '{author_avatar.get('alt')}'"
        assert author_avatar.get("width") == "40", "Avatar should have width='40'"
        assert author_avatar.get("height") == "40", "Avatar should have height='40'"

    def test_individual_post_shows_author_name(self, hugo_site, get_post_html_fixture):
        """Test that individual posts show author names as links (hideAuthor: false)."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        # Look for author name link
        author_links = soup.find_all("a", class_="author")
        assert len(author_links) >= 1, "Individual post should have author link(s)"

        # Find the text author link (not just the avatar link)
        text_author_link = None
        for link in author_links:
            if link.get_text().strip() == "Björn Andersson":
                text_author_link = link
                break

        assert (
            text_author_link is not None
        ), "Should find author name link with 'Björn Andersson'"
        assert (
            text_author_link.get("href") == "/about"
        ), f"Author link should go to '/about' but was '{text_author_link.get('href')}'"

    def test_homepage_hides_author_avatars(self, hugo_site, parse_html_fixture):
        """Test that homepage listing hides author avatars (hideAuthor: true)."""
        homepage = parse_html_fixture(hugo_site / "index.html")

        # Homepage should not show author avatars in post listings
        author_avatars = homepage.find_all("img", class_="author-avatar")
        assert (
            len(author_avatars) == 0
        ), f"Homepage should hide author avatars but found {len(author_avatars)}"

    def test_homepage_hides_author_names(self, hugo_site, parse_html_fixture):
        """Test that homepage listing hides author names (hideAuthor: true)."""
        homepage = parse_html_fixture(hugo_site / "index.html")

        # Homepage should not show author names in post listings
        author_links = homepage.find_all("a", class_="author")
        assert (
            len(author_links) == 0
        ), f"Homepage should hide author names but found {len(author_links)}"

    def test_blog_listing_hides_author_avatars(self, hugo_site, parse_html_fixture):
        """Test that blog listing page hides author avatars (hideAuthor: true)."""
        blog_listing_path = hugo_site / "blog/index.html"
        if not blog_listing_path.exists():
            pytest.skip("Blog listing page not found")

        blog_listing = parse_html_fixture(blog_listing_path)

        # Blog listing should not show author avatars
        author_avatars = blog_listing.find_all("img", class_="author-avatar")
        assert (
            len(author_avatars) == 0
        ), f"Blog listing should hide author avatars but found {len(author_avatars)}"

    def test_blog_listing_hides_author_names(self, hugo_site, parse_html_fixture):
        """Test that blog listing page hides author names (hideAuthor: true)."""
        blog_listing_path = hugo_site / "blog/index.html"
        if not blog_listing_path.exists():
            pytest.skip("Blog listing page not found")

        blog_listing = parse_html_fixture(blog_listing_path)

        # Blog listing should not show author names
        author_links = blog_listing.find_all("a", class_="author")
        assert (
            len(author_links) == 0
        ), f"Blog listing should hide author names but found {len(author_links)}"

    def test_tag_pages_hide_author_avatars(self, hugo_site, parse_html_fixture):
        """Test that tag pages hide author avatars (hideAuthor: true)."""
        # Look for any tag page
        tags_dir = hugo_site / "tags"
        if not tags_dir.exists():
            pytest.skip("Tags directory not found")

        # Find a tag page to test
        tag_page = None
        for tag_dir in tags_dir.iterdir():
            if tag_dir.is_dir():
                index_file = tag_dir / "index.html"
                if index_file.exists():
                    tag_page = index_file
                    break

        if tag_page is None:
            pytest.skip("No tag pages found")

        soup = parse_html_fixture(tag_page)

        # Tag pages should not show author avatars in post listings
        author_avatars = soup.find_all("img", class_="author-avatar")
        assert (
            len(author_avatars) == 0
        ), f"Tag page should hide author avatars but found {len(author_avatars)}"

    def test_tag_pages_hide_author_names(self, hugo_site, parse_html_fixture):
        """Test that tag pages hide author names (hideAuthor: true)."""
        # Look for any tag page
        tags_dir = hugo_site / "tags"
        if not tags_dir.exists():
            pytest.skip("Tags directory not found")

        # Find a tag page to test
        tag_page = None
        for tag_dir in tags_dir.iterdir():
            if tag_dir.is_dir():
                index_file = tag_dir / "index.html"
                if index_file.exists():
                    tag_page = index_file
                    break

        if tag_page is None:
            pytest.skip("No tag pages found")

        soup = parse_html_fixture(tag_page)

        # Tag pages should not show author names in post listings
        author_links = soup.find_all("a", class_="author")
        assert (
            len(author_links) == 0
        ), f"Tag page should hide author names but found {len(author_links)}"

    def test_all_individual_posts_show_authors(
        self, hugo_site, parse_html_fixture, get_all_posts_fixture
    ):
        """Test that all individual posts show author information (hideAuthor: false)."""
        posts = get_all_posts_fixture()
        assert len(posts) > 0, "Should find blog posts"

        for post_path in posts:
            soup = parse_html_fixture(post_path)

            # Skip redirect pages (they have refresh meta tag and minimal content)
            if soup.find("meta", attrs={"http-equiv": "refresh"}):
                continue

            # Each real post should have a meta section
            meta_div = soup.find("div", class_="meta")
            assert meta_div is not None, f"Post {post_path} should have meta section"

            # Should have either author avatar or author name (or both)
            author_avatar = soup.find("img", class_="author-avatar")
            author_links = soup.find_all("a", class_="author")

            # At minimum, should have author name link
            # (avatar might not exist if author doesn't have one or file doesn't exist)
            assert (
                len(author_links) > 0
            ), f"Post {post_path} should have author name link"

    def test_author_link_consistency(self, hugo_site, get_post_html_fixture):
        """Test that author links are consistent between avatar and name."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        # Get all author links
        author_links = soup.find_all("a", class_="author")
        assert len(author_links) >= 1, "Should have author links"

        # All author links should point to the same URL
        urls = [link.get("href") for link in author_links]
        unique_urls = set(urls)
        assert (
            len(unique_urls) == 1
        ), f"All author links should point to same URL, but found: {unique_urls}"

        # Should point to the author's custom page
        assert (
            urls[0] == "/about"
        ), f"Author links should point to '/about' but pointed to '{urls[0]}'"

    def test_meta_content_structure(self, hugo_site, get_post_html_fixture):
        """Test that meta section has proper structure."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        # Find meta section
        meta_div = soup.find("div", class_="meta")
        assert meta_div is not None, "Should have meta div"

        # Should have meta-content div
        meta_content = meta_div.find("div", class_="meta-content")
        assert meta_content is not None, "Should have meta-content div"

        # Should have meta-line divs
        meta_lines = meta_content.find_all("div", class_="meta-line")
        assert len(meta_lines) >= 1, "Should have at least one meta-line div"

        # First meta-line should contain author info (when not hidden)
        first_meta_line = meta_lines[0]
        author_link = first_meta_line.find("a", class_="author")
        assert author_link is not None, "First meta-line should contain author link"

    def test_author_avatar_container_structure(self, hugo_site, get_post_html_fixture):
        """Test that author avatar has proper container structure."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        # Find avatar container
        meta_avatar = soup.find("div", class_="meta-avatar")
        if meta_avatar is not None:  # Avatar might not exist if file missing
            # Should contain an author link
            avatar_link = meta_avatar.find("a", class_="author")
            assert avatar_link is not None, "meta-avatar should contain author link"

            # Link should contain the avatar image
            avatar_img = avatar_link.find("img", class_="author-avatar")
            assert avatar_img is not None, "Avatar link should contain avatar image"

    def test_post_without_author_still_renders(
        self, hugo_site, parse_html_fixture, get_all_posts_fixture
    ):
        """Test that posts without explicit authors still render properly."""
        posts = get_all_posts_fixture()

        # Most posts should have authors, but let's verify the structure handles it gracefully
        real_posts_checked = 0
        for post_path in posts:
            soup = parse_html_fixture(post_path)

            # Skip redirect pages (they have refresh meta tag and minimal content)
            if soup.find("meta", attrs={"http-equiv": "refresh"}):
                continue

            real_posts_checked += 1
            if real_posts_checked > 5:  # Check first 5 real posts
                break

            # Should always have meta section
            meta_div = soup.find("div", class_="meta")
            assert meta_div is not None, f"Post {post_path} should have meta section"

            # Should always have meta-content
            meta_content = meta_div.find("div", class_="meta-content")
            assert (
                meta_content is not None
            ), f"Post {post_path} should have meta-content"

            # Should always have at least one meta-line (for date/time)
            meta_lines = meta_content.find_all("div", class_="meta-line")
            assert (
                len(meta_lines) >= 1
            ), f"Post {post_path} should have at least one meta-line"

    def test_multiple_authors_support(
        self, hugo_site, parse_html_fixture, get_all_posts_fixture
    ):
        """Test that the template can handle multiple authors properly."""
        # Even if all current posts have single authors, the template should handle multiple authors
        posts = get_all_posts_fixture()

        real_posts_checked = 0
        for post_path in posts:
            soup = parse_html_fixture(post_path)

            # Skip redirect pages (they have refresh meta tag and minimal content)
            if soup.find("meta", attrs={"http-equiv": "refresh"}):
                continue

            real_posts_checked += 1
            if real_posts_checked > 3:  # Check first 3 real posts
                break

            # Find author section
            meta_div = soup.find("div", class_="meta")
            if meta_div:
                author_links = meta_div.find_all("a", class_="author")
                # Should have at least one author link
                assert (
                    len(author_links) >= 1
                ), f"Post {post_path} should have at least one author"

                # All author links should be valid
                for link in author_links:
                    assert link.get("href") is not None, "Author links should have href"
                    # Some author links contain only images (avatar links), others contain text
                    # We just need to ensure the link has some content (either text or img)
                    has_text = bool(link.get_text().strip())
                    has_img = link.find("img") is not None
                    assert (
                        has_text or has_img
                    ), "Author links should have either text or image content"

    def test_author_avatar_alt_text_accessibility(
        self, hugo_site, get_post_html_fixture
    ):
        """Test that author avatars have proper alt text for accessibility."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        author_avatar = soup.find("img", class_="author-avatar")
        if author_avatar is not None:
            alt_text = author_avatar.get("alt")
            assert alt_text is not None, "Author avatar should have alt text"
            assert len(alt_text.strip()) > 0, "Alt text should not be empty"
            assert "Björn Andersson" in alt_text, "Alt text should contain author name"

    def test_individual_post_author_metadata_consistency(
        self, hugo_site, get_post_html_fixture
    ):
        """Test that author metadata is consistent across different parts of individual posts."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        # Check meta tag author
        meta_author = soup.find("meta", attrs={"name": "author"})
        assert meta_author is not None, "Should have meta author tag"
        assert (
            meta_author.get("content") == "Björn Andersson"
        ), f"Meta author should be 'Björn Andersson' but was '{meta_author.get('content')}'"

        # Check Twitter card author
        twitter_author = soup.find("meta", attrs={"name": "twitter:data1"})
        if twitter_author:
            assert (
                twitter_author.get("content") == "Björn Andersson"
            ), f"Twitter author should be 'Björn Andersson' but was '{twitter_author.get('content')}'"

        # Check that visible author matches meta author
        author_links = soup.find_all("a", class_="author")
        visible_author = None
        for link in author_links:
            text = link.get_text().strip()
            if text == "Björn Andersson":
                visible_author = text
                break

        assert (
            visible_author == "Björn Andersson"
        ), "Visible author should match meta author"
