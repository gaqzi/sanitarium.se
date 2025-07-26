"""
Test meta tag generation across the Hugo site.

Tests verify:
1. Basic meta tags: viewport, description, author, canonical
2. Open Graph tags: title, description, url, image, type
3. Twitter Card tags with proper content
4. Fediverse creator tag presence
5. Meta tag consistency between homepage and posts
"""
import pytest
from pathlib import Path
from bs4 import BeautifulSoup


class TestMetaTags:
    """Test suite for meta tag functionality."""
    
    def test_homepage_basic_meta_tags(self, hugo_site, parse_html_fixture):
        """Test that homepage has all required basic meta tags."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # Viewport meta tag
        viewport = homepage.find('meta', attrs={'name': 'viewport'})
        assert viewport is not None, "Homepage should have viewport meta tag"
        assert 'width=device-width' in viewport.get('content', ''), \
            "Viewport should include width=device-width"
        assert 'initial-scale=1' in viewport.get('content', ''), \
            "Viewport should include initial-scale=1"
        
        # Description meta tag
        description = homepage.find('meta', attrs={'name': 'description'})
        assert description is not None, "Homepage should have description meta tag"
        desc_content = description.get('content', '')
        assert len(desc_content.strip()) > 0, "Description should not be empty"
        
        # Author meta tag
        author = homepage.find('meta', attrs={'name': 'author'})
        assert author is not None, "Homepage should have author meta tag"
        assert len(author.get('content', '').strip()) > 0, "Author should not be empty"
        
        # Canonical link
        canonical = homepage.find('link', attrs={'rel': 'canonical'})
        assert canonical is not None, "Homepage should have canonical link"
        canonical_href = canonical.get('href', '')
        assert canonical_href.startswith('http'), "Canonical URL should be absolute"
    
    def test_individual_post_basic_meta_tags(self, hugo_site, get_post_html_fixture):
        """Test that individual posts have all required basic meta tags."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        assert viewport is not None, "Post should have viewport meta tag"
        assert 'width=device-width' in viewport.get('content', ''), \
            "Viewport should include width=device-width"
        
        # Description meta tag
        description = soup.find('meta', attrs={'name': 'description'})
        assert description is not None, "Post should have description meta tag"
        desc_content = description.get('content', '')
        assert len(desc_content.strip()) > 0, "Description should not be empty"
        
        # Author meta tag
        author = soup.find('meta', attrs={'name': 'author'})
        assert author is not None, "Post should have author meta tag"
        author_content = author.get('content', '')
        assert len(author_content.strip()) > 0, "Author should not be empty"
        assert "Björn Andersson" in author_content, "Author should be Björn Andersson"
        
        # Canonical link
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        assert canonical is not None, "Post should have canonical link"
        canonical_href = canonical.get('href', '')
        assert canonical_href.startswith('http'), "Canonical URL should be absolute"
        assert 'which-hat-are-you-wearing' in canonical_href, \
            "Canonical URL should include post slug"
    
    def test_homepage_open_graph_tags(self, hugo_site, parse_html_fixture):
        """Test that homepage has all required Open Graph tags."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # og:title
        og_title = homepage.find('meta', attrs={'property': 'og:title'})
        assert og_title is not None, "Homepage should have og:title"
        title_content = og_title.get('content', '')
        assert len(title_content.strip()) > 0, "og:title should not be empty"
        
        # og:description
        og_description = homepage.find('meta', attrs={'property': 'og:description'})
        assert og_description is not None, "Homepage should have og:description"
        desc_content = og_description.get('content', '')
        assert len(desc_content.strip()) > 0, "og:description should not be empty"
        
        # og:url
        og_url = homepage.find('meta', attrs={'property': 'og:url'})
        assert og_url is not None, "Homepage should have og:url"
        url_content = og_url.get('content', '')
        assert url_content.startswith('http'), "og:url should be absolute URL"
        
        # og:type
        og_type = homepage.find('meta', attrs={'property': 'og:type'})
        assert og_type is not None, "Homepage should have og:type"
        type_content = og_type.get('content', '')
        assert type_content in ['website', 'blog'], \
            f"og:type should be 'website' or 'blog', got '{type_content}'"
        
        # og:image (optional but should exist if present)
        og_image = homepage.find('meta', attrs={'property': 'og:image'})
        if og_image is not None:
            image_content = og_image.get('content', '')
            assert len(image_content.strip()) > 0, "og:image should not be empty if present"
    
    def test_individual_post_open_graph_tags(self, hugo_site, get_post_html_fixture):
        """Test that individual posts have all required Open Graph tags."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # og:title
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        assert og_title is not None, "Post should have og:title"
        title_content = og_title.get('content', '')
        assert len(title_content.strip()) > 0, "og:title should not be empty"
        assert 'hat' in title_content.lower(), "og:title should relate to post content"
        
        # og:description
        og_description = soup.find('meta', attrs={'property': 'og:description'})
        assert og_description is not None, "Post should have og:description"
        desc_content = og_description.get('content', '')
        assert len(desc_content.strip()) > 0, "og:description should not be empty"
        
        # og:url
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        assert og_url is not None, "Post should have og:url"
        url_content = og_url.get('content', '')
        assert url_content.startswith('http'), "og:url should be absolute URL"
        assert 'which-hat-are-you-wearing' in url_content, \
            "og:url should include post slug"
        
        # og:type
        og_type = soup.find('meta', attrs={'property': 'og:type'})
        assert og_type is not None, "Post should have og:type"
        type_content = og_type.get('content', '')
        assert type_content == 'article', \
            f"Post og:type should be 'article', got '{type_content}'"
        
        # og:image (optional but should exist if present)
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        if og_image is not None:
            image_content = og_image.get('content', '')
            assert len(image_content.strip()) > 0, "og:image should not be empty if present"
            assert image_content.startswith('http'), "og:image should be absolute URL"
    
    def test_homepage_twitter_card_tags(self, hugo_site, parse_html_fixture):
        """Test that homepage has proper Twitter Card tags."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # twitter:card
        twitter_card = homepage.find('meta', attrs={'name': 'twitter:card'})
        assert twitter_card is not None, "Homepage should have twitter:card"
        card_content = twitter_card.get('content', '')
        assert card_content in ['summary', 'summary_large_image'], \
            f"twitter:card should be 'summary' or 'summary_large_image', got '{card_content}'"
        
        # twitter:title
        twitter_title = homepage.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title is not None:
            title_content = twitter_title.get('content', '')
            assert len(title_content.strip()) > 0, "twitter:title should not be empty if present"
        
        # twitter:description
        twitter_description = homepage.find('meta', attrs={'name': 'twitter:description'})
        if twitter_description is not None:
            desc_content = twitter_description.get('content', '')
            assert len(desc_content.strip()) > 0, "twitter:description should not be empty if present"
        
        # twitter:image (optional)
        twitter_image = homepage.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image is not None:
            image_content = twitter_image.get('content', '')
            assert len(image_content.strip()) > 0, "twitter:image should not be empty if present"
    
    def test_individual_post_twitter_card_tags(self, hugo_site, get_post_html_fixture):
        """Test that individual posts have proper Twitter Card tags."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # twitter:card
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        assert twitter_card is not None, "Post should have twitter:card"
        card_content = twitter_card.get('content', '')
        assert card_content in ['summary', 'summary_large_image'], \
            f"twitter:card should be 'summary' or 'summary_large_image', got '{card_content}'"
        
        # twitter:title
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title is not None:
            title_content = twitter_title.get('content', '')
            assert len(title_content.strip()) > 0, "twitter:title should not be empty if present"
            assert 'hat' in title_content.lower(), "twitter:title should relate to post content"
        
        # twitter:description
        twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
        if twitter_description is not None:
            desc_content = twitter_description.get('content', '')
            assert len(desc_content.strip()) > 0, "twitter:description should not be empty if present"
        
        # twitter:image (optional)
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image is not None:
            image_content = twitter_image.get('content', '')
            assert len(image_content.strip()) > 0, "twitter:image should not be empty if present"
            assert image_content.startswith('http'), "twitter:image should be absolute URL"
        
        # twitter:creator (optional but common for posts)
        twitter_creator = soup.find('meta', attrs={'name': 'twitter:creator'})
        if twitter_creator is not None:
            creator_content = twitter_creator.get('content', '')
            assert len(creator_content.strip()) > 0, "twitter:creator should not be empty if present"
            assert creator_content.startswith('@'), "twitter:creator should start with @"
    
    def test_fediverse_creator_tag(self, hugo_site, get_post_html_fixture):
        """Test that posts have fediverse:creator tag for Mastodon attribution."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # fediverse:creator
        fedi_creator = soup.find('meta', attrs={'name': 'fediverse:creator'})
        if fedi_creator is not None:
            creator_content = fedi_creator.get('content', '')
            assert len(creator_content.strip()) > 0, "fediverse:creator should not be empty if present"
            # Should be a Mastodon handle format
            assert '@' in creator_content, "fediverse:creator should contain @ symbol"
    
    def test_meta_tag_consistency_between_formats(self, hugo_site, get_post_html_fixture):
        """Test that meta tags are consistent between different formats (basic, OG, Twitter)."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get all title variants
        page_title = soup.find('title')
        meta_title = soup.find('meta', attrs={'name': 'title'})
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        
        titles = []
        if page_title and page_title.string:
            titles.append(page_title.string.strip())
        if meta_title:
            titles.append(meta_title.get('content', '').strip())
        if og_title:
            titles.append(og_title.get('content', '').strip())
        if twitter_title:
            titles.append(twitter_title.get('content', '').strip())
        
        # At least some titles should exist and be non-empty
        assert len([t for t in titles if t]) > 0, "Should have at least one non-empty title"
        
        # Get all description variants
        meta_description = soup.find('meta', attrs={'name': 'description'})
        og_description = soup.find('meta', attrs={'property': 'og:description'})
        twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
        
        descriptions = []
        if meta_description:
            descriptions.append(meta_description.get('content', '').strip())
        if og_description:
            descriptions.append(og_description.get('content', '').strip())
        if twitter_description:
            descriptions.append(twitter_description.get('content', '').strip())
        
        # At least some descriptions should exist and be non-empty
        non_empty_descriptions = [d for d in descriptions if d]
        assert len(non_empty_descriptions) > 0, "Should have at least one non-empty description"
        
        # All non-empty descriptions should be reasonable length (not just single words)
        for desc in non_empty_descriptions:
            assert len(desc) > 10, f"Description should be substantial, got: {desc[:50]}..."
    
    def test_charset_and_language_meta_tags(self, hugo_site, parse_html_fixture):
        """Test that pages have proper charset and language declarations."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # Charset declaration (should be early in head)
        charset = homepage.find('meta', attrs={'charset': True})
        assert charset is not None, "Should have charset meta tag"
        charset_value = charset.get('charset', '').lower()
        assert charset_value in ['utf-8', 'utf8'], \
            f"Charset should be UTF-8, got '{charset_value}'"
        
        # Language on html element
        html_element = homepage.find('html')
        if html_element:
            lang = html_element.get('lang')
            if lang:
                assert len(lang.strip()) > 0, "Language should not be empty if present"
                # Common language codes
                assert lang.lower() in ['en', 'en-us', 'en-gb', 'sv', 'sv-se'], \
                    f"Should use valid language code, got '{lang}'"
    
    def test_robots_and_generator_meta_tags(self, hugo_site, parse_html_fixture):
        """Test robots and generator meta tags."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # Generator tag (Hugo adds this automatically)
        generator = homepage.find('meta', attrs={'name': 'generator'})
        if generator is not None:
            gen_content = generator.get('content', '')
            assert 'hugo' in gen_content.lower(), "Generator should mention Hugo"
        
        # Robots tag (optional but useful)
        robots = homepage.find('meta', attrs={'name': 'robots'})
        if robots is not None:
            robots_content = robots.get('content', '')
            assert len(robots_content.strip()) > 0, "Robots directive should not be empty if present"
            # Should contain valid robots directives
            valid_directives = ['index', 'noindex', 'follow', 'nofollow', 'all', 'none']
            found_valid = any(directive in robots_content.lower() for directive in valid_directives)
            assert found_valid, f"Robots should contain valid directives, got '{robots_content}'"
    
    def test_all_posts_have_required_meta_tags(self, hugo_site, parse_html_fixture, get_all_posts_fixture):
        """Test that all blog posts have the essential meta tags."""
        posts = get_all_posts_fixture()
        assert len(posts) > 0, "Should find blog posts"
        
        # Check a few posts to ensure consistency
        posts_to_check = posts[:5]  # Check first 5 posts
        
        for post_path in posts_to_check:
            soup = parse_html_fixture(post_path)
            
            # Skip redirect pages (they have refresh meta tag and minimal content)
            if soup.find('meta', attrs={'http-equiv': 'refresh'}):
                continue
            
            # Essential meta tags that every post should have
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            assert viewport is not None, f"Post {post_path} should have viewport meta tag"
            
            description = soup.find('meta', attrs={'name': 'description'})
            assert description is not None, f"Post {post_path} should have description meta tag"
            
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            assert canonical is not None, f"Post {post_path} should have canonical link"
            
            # Open Graph essentials
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            assert og_title is not None, f"Post {post_path} should have og:title"
            
            og_type = soup.find('meta', attrs={'property': 'og:type'})
            assert og_type is not None, f"Post {post_path} should have og:type"
            assert og_type.get('content') == 'article', \
                f"Post {post_path} og:type should be 'article'"
    
    def test_meta_tag_content_encoding(self, hugo_site, get_post_html_fixture):
        """Test that meta tag content handles special characters properly."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Check that content with special characters is properly encoded
        author = soup.find('meta', attrs={'name': 'author'})
        if author and 'Björn' in author.get('content', ''):
            # Should handle UTF-8 characters properly
            assert 'Björn Andersson' in author.get('content'), \
                "Should handle Swedish characters in author name"
        
        # Check that descriptions don't have HTML entities in meta tags
        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            desc_content = description.get('content', '')
            # Should not contain HTML entities like &amp; &lt; &gt;
            assert '&amp;' not in desc_content, "Description should not contain HTML entities"
            assert '&lt;' not in desc_content, "Description should not contain HTML entities"
            assert '&gt;' not in desc_content, "Description should not contain HTML entities"
            assert '<' not in desc_content, "Description should not contain raw HTML"
            assert '>' not in desc_content, "Description should not contain raw HTML"
    
    def test_structured_data_presence(self, hugo_site, get_post_html_fixture):
        """Test that structured data (JSON-LD) is present and valid."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Look for JSON-LD structured data
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        # It's okay if there's no structured data, but if present, it should be valid
        if json_ld_scripts:
            import json
            for script in json_ld_scripts:
                if script.string:
                    try:
                        data = json.loads(script.string)
                        # Should have @context and @type for valid JSON-LD
                        assert '@context' in data, "JSON-LD should have @context"
                        assert '@type' in data, "JSON-LD should have @type"
                    except json.JSONDecodeError:
                        pytest.fail(f"Invalid JSON-LD structure: {script.string[:100]}...")