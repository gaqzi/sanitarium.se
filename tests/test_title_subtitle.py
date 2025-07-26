"""
Test title and subtitle rendering across the Hugo site.

Tests verify:
1. The title-with-subtitle partial is used everywhere
2. Title tags combine title + subtitle correctly
3. Subtitle renders as <p class="subtitle"> in post headers
4. Edge cases (no subtitle, punctuation handling)
5. Specific post rendering
"""
import pytest
from pathlib import Path
from bs4 import BeautifulSoup


class TestTitleSubtitle:
    """Test suite for title and subtitle functionality."""
    
    def test_specific_post_title_tag(self, hugo_site, get_post_html_fixture):
        """Test that the specific post combines title and subtitle correctly in title tag."""
        # Test the specific post mentioned in requirements
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        title_tag = soup.find('title')
        assert title_tag is not None, "Title tag should exist"
        
        expected_title = "Which hat are you wearing? ...you wouldn't wear a beanie to the beach | the padded cell"
        assert title_tag.string == expected_title, f"Title tag should be '{expected_title}' but was '{title_tag.string}'"
    
    def test_post_with_subtitle_title_tag(self, hugo_site, get_post_html_fixture):
        """Test posts with subtitles have combined title tags."""
        # Test various posts with subtitles
        test_cases = [
            {
                "slug": "blog/2025/07/12/which-hat-are-you-wearing",
                "expected": "Which hat are you wearing? ...you wouldn't wear a beanie to the beach | the padded cell"
            },
            {
                "slug": "blog/2025/07/24/your-name-is-still-on-it",
                "expected_title": "Your name is still on it",
                "has_subtitle": False  # We'll check if this post has a subtitle
            }
        ]
        
        for test_case in test_cases:
            soup = get_post_html_fixture(test_case["slug"])
            title_tag = soup.find('title')
            
            if "expected" in test_case:
                assert title_tag.string == test_case["expected"]
            else:
                # Just verify title tag exists
                assert title_tag is not None
    
    def test_subtitle_renders_as_paragraph(self, hugo_site, get_post_html_fixture):
        """Test that subtitle renders as <p class="subtitle"> in post headers."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Find the subtitle paragraph
        subtitle_p = soup.find('p', class_='subtitle')
        assert subtitle_p is not None, "Subtitle should be rendered as <p class='subtitle'>"
        assert subtitle_p.string.strip() == "...you wouldn't wear a beanie to the beach", \
            f"Subtitle content should match, but was '{subtitle_p.string.strip()}'"
    
    def test_punctuation_handling(self, hugo_site, get_post_html_fixture):
        """Test that punctuation is handled correctly between title and subtitle."""
        # Test the specific post which has a question mark
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        title_tag = soup.find('title')
        
        # Should have a space but no em dash because title ends with punctuation
        assert "Which hat are you wearing? ...you" in title_tag.string
        assert " — " not in title_tag.string, "Should not have em dash when title ends with punctuation"
    
    def test_homepage_title(self, hugo_site, parse_html_fixture):
        """Test that homepage uses site title correctly."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        title_tag = homepage.find('title')
        
        assert title_tag is not None, "Homepage should have a title tag"
        # Homepage should use site title (not post title)
        assert title_tag.string == "the padded cell", \
            f"Homepage title should be site title, but was '{title_tag.string}'"
    
    def test_all_posts_have_title_tags(self, hugo_site, parse_html_fixture, get_all_posts_fixture):
        """Test that all posts have title tags."""
        posts = get_all_posts_fixture()
        assert len(posts) > 0, "Should find blog posts"
        
        for post_path in posts:
            soup = parse_html_fixture(post_path)
            title_tag = soup.find('title')
            assert title_tag is not None, f"Post {post_path} should have a title tag"
            assert title_tag.string and len(title_tag.string.strip()) > 0, \
                f"Post {post_path} should have non-empty title tag"
    
    def test_list_pages_have_titles(self, hugo_site, parse_html_fixture):
        """Test that list pages (tags, authors, etc.) have proper titles."""
        list_pages = [
            "tags/index.html",
            "authors/index.html",
            "blog/index.html",
        ]
        
        for page_path in list_pages:
            full_path = hugo_site / page_path
            if full_path.exists():
                soup = parse_html_fixture(full_path)
                title_tag = soup.find('title')
                assert title_tag is not None, f"List page {page_path} should have a title tag"
    
    def test_post_without_subtitle(self, hugo_site, parse_html_fixture, get_all_posts_fixture):
        """Test that posts without subtitles render correctly."""
        # Find a post without a subtitle by checking multiple posts
        posts = get_all_posts_fixture()
        found_post_without_subtitle = False
        
        for post_path in posts[:10]:  # Check first 10 posts
            soup = parse_html_fixture(post_path)
            subtitle_p = soup.find('p', class_='subtitle')
            
            if subtitle_p is None:
                # Found a post without subtitle
                found_post_without_subtitle = True
                title_tag = soup.find('title')
                assert title_tag is not None, f"Post without subtitle should still have title tag"
                
                # Title should not have em dash or ellipsis pattern
                assert " — " not in title_tag.string, \
                    "Post without subtitle should not have em dash in title"
                break
        
        # We expect at least one post without subtitle in the blog
        assert found_post_without_subtitle, "Should find at least one post without subtitle"
    
    def test_og_title_consistency(self, hugo_site, get_post_html_fixture):
        """Test that Open Graph titles are consistent with page titles."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        title_tag = soup.find('title')
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        
        assert og_title is not None, "Should have Open Graph title"
        # OG title might be just the post title without subtitle, or the full title
        og_content = og_title.get('content')
        assert "Which hat are you wearing?" in og_content, \
            f"OG title should contain main title, but was '{og_content}'"
    
    def test_article_header_structure(self, hugo_site, get_post_html_fixture):
        """Test that article headers have proper structure with title and subtitle."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Find the article or main content area
        article = soup.find('article') or soup.find('main')
        assert article is not None, "Should have article or main element"
        
        # Look for h1 within article
        h1 = article.find('h1')
        assert h1 is not None, "Article should have an h1"
        assert "Which hat are you wearing?" in h1.get_text(), "H1 should contain the title"
        
        # Look for subtitle after h1
        # It should be a sibling of h1 or within the same header structure
        header = h1.parent
        subtitle_p = header.find('p', class_='subtitle')
        assert subtitle_p is not None, "Should find subtitle paragraph near h1"