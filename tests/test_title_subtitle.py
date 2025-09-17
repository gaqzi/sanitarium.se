"""
Test title and subtitle rendering across the Hugo site.

Tests verify:
1. Title tags combine title + subtitle correctly
2. Subtitle renders as <p class="subtitle"> in post headers
3. Edge cases (no subtitle, punctuation handling)
4. Homepage and list page titles
5. Open Graph and article structure consistency
"""

import typing
from dataclasses import dataclass

import pytest
from bs4 import BeautifulSoup


@dataclass
class TitleSubtitleTestCase:
    """Test case definition for title/subtitle combinations."""

    slug: str
    title: str
    subtitle: typing.Optional[str] = None
    has_punctuation: bool = False

    @property
    def expected_title_tag(self) -> str:
        """Generate expected title tag content."""
        if self.subtitle is None:
            return f"{self.title} | bjorn.now"

        if self.has_punctuation:
            return f"{self.title} {self.subtitle} | bjorn.now"
        else:
            return f"{self.title} — {self.subtitle} | bjorn.now"


def assert_title_tag(soup: BeautifulSoup, expected_title: str) -> None:
    """Assert that the HTML title tag matches the expected value."""
    title_tag = soup.find("title")
    assert title_tag is not None, "Title tag should exist"
    assert (
        title_tag.string == expected_title
    ), f"Title tag should be '{expected_title}' but was '{title_tag.string}'"


def assert_subtitle_element(soup: BeautifulSoup, expected_subtitle: str) -> None:
    """Assert that the subtitle renders as <p class="subtitle"> with expected content."""
    subtitle_p = soup.find("p", class_="subtitle")
    assert subtitle_p is not None, "Subtitle should be rendered as <p class='subtitle'>"
    assert (
        subtitle_p.string.strip() == expected_subtitle
    ), f"Subtitle content should be '{expected_subtitle}', but was '{subtitle_p.string.strip()}'"


def assert_title_subtitle_combination(
    soup: BeautifulSoup,
    title: str,
    subtitle: typing.Optional[str] = None,
    has_punctuation: bool = False,
) -> None:
    """Assert that title and subtitle are combined correctly in the title tag."""
    if subtitle is None:
        # Post without subtitle - should just be title + site name
        expected_title = f"{title} | bjorn.now"
        assert_title_tag(soup, expected_title)

        # Should not have em dash
        title_tag = soup.find("title")
        assert (
            " — " not in title_tag.string
        ), "Post without subtitle should not have em dash in title"
    else:
        # Post with subtitle
        if has_punctuation:
            # Title ends with punctuation - use space only
            expected_title = f"{title} {subtitle} | bjorn.now"
        else:
            # Title doesn't end with punctuation - use em dash
            expected_title = f"{title} — {subtitle} | bjorn.now"

        assert_title_tag(soup, expected_title)
        assert_subtitle_element(soup, subtitle)


def assert_og_title(soup: BeautifulSoup, expected_og_title: str) -> None:
    """Assert that Open Graph title meta tag matches expected value."""
    og_title = soup.find("meta", attrs={"property": "og:title"})
    assert og_title is not None, "Should have Open Graph title"
    og_content = og_title.get("content")
    assert (
        expected_og_title in og_content
    ), f"OG title should contain '{expected_og_title}', but was '{og_content}'"


def assert_article_structure(soup: BeautifulSoup, expected_h1_text: str) -> None:
    """Assert that article has proper header structure with h1 and optional subtitle."""
    # Find the article or main content area
    article = soup.find("article") or soup.find("main")
    assert article is not None, "Should have article or main element"

    # Look for h1 within article
    h1 = article.find("h1")
    assert h1 is not None, "Article should have an h1"
    assert expected_h1_text in h1.get_text(), f"H1 should contain '{expected_h1_text}'"


def assert_no_em_dash_in_title(soup: BeautifulSoup) -> None:
    """Assert that the title tag does not contain an em dash."""
    title_tag = soup.find("title")
    assert title_tag is not None, "Title tag should exist"
    assert " — " not in title_tag.string, "Title should not contain em dash"


def assert_em_dash_in_title(soup: BeautifulSoup) -> None:
    """Assert that the title tag contains an em dash (for title-subtitle separation)."""
    title_tag = soup.find("title")
    assert title_tag is not None, "Title tag should exist"
    assert (
        " — " in title_tag.string
    ), "Title should contain em dash for title-subtitle separation"


# Test data for parametrized tests
TITLE_SUBTITLE_TEST_CASES = [
    TitleSubtitleTestCase(
        slug="blog/2025/07/12/which-hat-are-you-wearing",
        title="Which hat are you wearing?",
        subtitle="...you wouldn't wear a beanie to the beach",
        has_punctuation=True,
    ),
    TitleSubtitleTestCase(
        slug="blog/2025/07/24/your-name-is-still-on-it",
        title="Your name is still on it",
        subtitle="learning to ride the AI motorcycle without crashing",
        has_punctuation=False,
    ),
    TitleSubtitleTestCase(
        slug="blog/2010/12/04/howto-satta-upp-en-wikileaksspegling",
        title="How to: Sätta upp en Wikileaksspegling",
        subtitle=None,  # Post without subtitle
    ),
]

LIST_PAGE_TEST_CASES = [
    ("tags/index.html", "Tags | bjorn.now"),
    ("authors/index.html", "Authors | bjorn.now"),
    ("blog/index.html", "Posts | bjorn.now"),
]


class TestTitleSubtitle:
    """Test suite for title and subtitle functionality."""

    @pytest.mark.parametrize(
        "test_case", TITLE_SUBTITLE_TEST_CASES, ids=lambda tc: tc.slug.split("/")[-1]
    )
    def test_title_subtitle_combinations(
        self, hugo_site, get_post_html_fixture, test_case
    ):
        """Test representative posts with different title/subtitle patterns."""
        soup = get_post_html_fixture(test_case.slug)
        assert_title_subtitle_combination(
            soup,
            test_case.title,
            test_case.subtitle,
            test_case.has_punctuation,
        )

    def test_em_dash_formatting(self, hugo_site, get_post_html_fixture):
        """Test that posts without ending punctuation use em-dash between title and subtitle."""
        soup = get_post_html_fixture(
            "blog/2025/07/07/working-with-gos-test-cache-on-ci"
        )

        # This post should have em-dash since title doesn't end with punctuation
        expected_title = "Working with Go's test cache on CI — be fast by avoiding work, while doing the important work | bjorn.now"
        assert_title_tag(soup, expected_title)
        assert_em_dash_in_title(soup)

    def test_punctuation_handling(self, hugo_site, get_post_html_fixture):
        """Test that punctuation is handled correctly between title and subtitle."""
        # Test post with question mark - should have space but no em dash
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        title_tag = soup.find("title")

        # Should have a space but no em dash because title ends with punctuation
        assert "Which hat are you wearing? ...you" in title_tag.string
        assert_no_em_dash_in_title(soup)

    def test_homepage_title(self, hugo_site, parse_html_fixture):
        """Test that homepage uses site title correctly."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        assert_title_tag(homepage, "bjorn.now")

    @pytest.mark.parametrize(
        "page_path,expected_title",
        LIST_PAGE_TEST_CASES,
        ids=lambda x: x[0] if isinstance(x, tuple) else x,
    )
    def test_list_page_titles(
        self, hugo_site, parse_html_fixture, page_path, expected_title
    ):
        """Test that list pages (tags, authors, etc.) have correct titles."""
        full_path = hugo_site / page_path
        if full_path.exists():
            soup = parse_html_fixture(full_path)
            assert_title_tag(soup, expected_title)
        else:
            pytest.skip(f"List page {page_path} does not exist")

    def test_og_title_consistency(self, hugo_site, get_post_html_fixture):
        """Test that Open Graph titles are consistent with page titles."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        assert_og_title(soup, "Which hat are you wearing?")

    def test_article_header_structure(self, hugo_site, get_post_html_fixture):
        """Test that article headers have proper structure with title and subtitle."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        assert_article_structure(soup, "Which hat are you wearing?")

        # Look for subtitle in article header structure
        article = soup.find("article") or soup.find("main")
        h1 = article.find("h1")
        header = h1.parent
        subtitle_p = header.find("p", class_="subtitle")
        assert subtitle_p is not None, "Should find subtitle paragraph near h1"
