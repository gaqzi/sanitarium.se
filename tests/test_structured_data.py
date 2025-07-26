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
import pytest
from pathlib import Path
from bs4 import BeautifulSoup


class TestStructuredData:
    """Test suite for JSON-LD structured data functionality."""
    
    def test_homepage_website_schema(self, hugo_site, parse_html_fixture):
        """Test that homepage has valid WebSite schema with required fields."""
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # Find JSON-LD script tags
        json_ld_scripts = homepage.find_all('script', attrs={'type': 'application/ld+json'})
        assert len(json_ld_scripts) > 0, "Homepage should have JSON-LD structured data"
        
        # Parse and validate JSON structure
        website_schema = None
        for script in json_ld_scripts:
            if script.string:
                try:
                    data = json.loads(script.string.strip())
                    if data.get('@type') == 'WebSite':
                        website_schema = data
                        break
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON-LD structure: {e}")
        
        assert website_schema is not None, "Homepage should have WebSite schema"
        
        # Validate required schema.org fields
        assert website_schema.get('@context') == 'https://schema.org', \
            "Should use schema.org context"
        assert website_schema.get('@type') == 'WebSite', \
            "Should have WebSite type"
        
        # Validate required WebSite properties
        assert 'url' in website_schema, "WebSite should have url property"
        assert website_schema['url'].startswith('http'), \
            "URL should be absolute"
        
        assert 'name' in website_schema, "WebSite should have name property"
        assert len(website_schema['name'].strip()) > 0, \
            "Name should not be empty"
        
        assert 'description' in website_schema, "WebSite should have description property"
        assert len(website_schema['description'].strip()) > 0, \
            "Description should not be empty"
        
        # Validate author information
        assert 'author' in website_schema, "WebSite should have author property"
        author = website_schema['author']
        assert author.get('@type') == 'Person', "Author should be a Person"
        assert 'name' in author, "Author should have name"
        assert len(author['name'].strip()) > 0, "Author name should not be empty"
        
        # Validate potential action (search)
        if 'potentialAction' in website_schema:
            action = website_schema['potentialAction']
            assert action.get('@type') == 'SearchAction', \
                "potentialAction should be SearchAction"
            assert 'target' in action, "SearchAction should have target"
            assert 'query-input' in action, "SearchAction should have query-input"
    
    def test_individual_post_blog_posting_schema(self, hugo_site, get_post_html_fixture):
        """Test that individual posts have valid BlogPosting schema with required fields."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Find JSON-LD script tags
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        assert len(json_ld_scripts) > 0, "Post should have JSON-LD structured data"
        
        # Parse and validate JSON structure
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                try:
                    data = json.loads(script.string.strip())
                    if data.get('@type') == 'BlogPosting':
                        blog_posting_schema = data
                        break
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON-LD structure: {e}")
        
        assert blog_posting_schema is not None, "Post should have BlogPosting schema"
        
        # Validate required schema.org fields
        assert blog_posting_schema.get('@context') == 'https://schema.org', \
            "Should use schema.org context"
        assert blog_posting_schema.get('@type') == 'BlogPosting', \
            "Should have BlogPosting type"
        
        # Validate required BlogPosting properties
        assert 'headline' in blog_posting_schema, "BlogPosting should have headline"
        headline = blog_posting_schema['headline']
        assert len(headline.strip()) > 0, "Headline should not be empty"
        assert 'hat' in headline.lower(), "Headline should relate to post content"
        
        assert 'author' in blog_posting_schema, "BlogPosting should have author"
        authors = blog_posting_schema['author']
        assert isinstance(authors, list), "Authors should be a list"
        assert len(authors) > 0, "Should have at least one author"
        
        # Validate first author
        author = authors[0]
        assert author.get('@type') == 'Person', "Author should be a Person"
        assert 'name' in author, "Author should have name"
        assert len(author['name'].strip()) > 0, "Author name should not be empty"
        
        assert 'datePublished' in blog_posting_schema, "BlogPosting should have datePublished"
        date_published = blog_posting_schema['datePublished']
        # Validate ISO 8601 date format
        try:
            datetime.fromisoformat(date_published.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"datePublished should be valid ISO 8601 format: {date_published}")
        
        # Validate other important properties
        assert 'url' in blog_posting_schema, "BlogPosting should have url"
        assert blog_posting_schema['url'].startswith('http'), \
            "URL should be absolute"
        assert 'which-hat-are-you-wearing' in blog_posting_schema['url'], \
            "URL should include post slug"
        
        assert 'description' in blog_posting_schema, "BlogPosting should have description"
        assert len(blog_posting_schema['description'].strip()) > 0, \
            "Description should not be empty"
    
    def test_blog_posting_publisher_information(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes proper publisher information."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get BlogPosting schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'BlogPosting':
                    blog_posting_schema = data
                    break
        
        assert blog_posting_schema is not None, "Should have BlogPosting schema"
        
        # Validate publisher information
        assert 'publisher' in blog_posting_schema, "BlogPosting should have publisher"
        publisher = blog_posting_schema['publisher']
        assert publisher.get('@type') == 'Organization', \
            "Publisher should be an Organization"
        assert 'name' in publisher, "Publisher should have name"
        assert len(publisher['name'].strip()) > 0, "Publisher name should not be empty"
        
        # Validate publisher logo
        if 'logo' in publisher:
            logo = publisher['logo']
            assert logo.get('@type') == 'ImageObject', \
                "Publisher logo should be ImageObject"
            assert 'url' in logo, "Logo should have url"
            assert logo['url'].startswith('http'), \
                "Logo URL should be absolute"
    
    def test_blog_posting_main_entity_of_page(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes mainEntityOfPage property."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get BlogPosting schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'BlogPosting':
                    blog_posting_schema = data
                    break
        
        assert blog_posting_schema is not None, "Should have BlogPosting schema"
        
        # Validate mainEntityOfPage
        assert 'mainEntityOfPage' in blog_posting_schema, \
            "BlogPosting should have mainEntityOfPage"
        main_entity = blog_posting_schema['mainEntityOfPage']
        assert main_entity.get('@type') == 'WebPage', \
            "mainEntityOfPage should be WebPage"
        assert '@id' in main_entity, "WebPage should have @id"
        assert main_entity['@id'].startswith('http'), \
            "WebPage @id should be absolute URL"
    
    def test_blog_posting_date_fields(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes proper date fields."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get BlogPosting schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'BlogPosting':
                    blog_posting_schema = data
                    break
        
        assert blog_posting_schema is not None, "Should have BlogPosting schema"
        
        # Validate datePublished (required)
        assert 'datePublished' in blog_posting_schema, \
            "BlogPosting should have datePublished"
        date_published = blog_posting_schema['datePublished']
        try:
            pub_date = datetime.fromisoformat(date_published.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"datePublished should be valid ISO 8601: {date_published}")
        
        # Validate dateModified (should be present)
        assert 'dateModified' in blog_posting_schema, \
            "BlogPosting should have dateModified"
        date_modified = blog_posting_schema['dateModified']
        try:
            mod_date = datetime.fromisoformat(date_modified.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"dateModified should be valid ISO 8601: {date_modified}")
        
        # dateModified should be >= datePublished
        assert mod_date >= pub_date, \
            "dateModified should be >= datePublished"
    
    def test_blog_posting_word_count(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema includes wordCount property."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get BlogPosting schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'BlogPosting':
                    blog_posting_schema = data
                    break
        
        assert blog_posting_schema is not None, "Should have BlogPosting schema"
        
        # Validate wordCount
        if 'wordCount' in blog_posting_schema:
            word_count = blog_posting_schema['wordCount']
            # Should be a number or string representation of a number
            try:
                count = int(word_count)
                assert count > 0, "Word count should be positive"
                assert count > 100, "Post should have substantial word count"
            except (ValueError, TypeError):
                pytest.fail(f"wordCount should be numeric: {word_count}")
    
    def test_json_ld_valid_json_syntax(self, hugo_site, get_post_html_fixture, parse_html_fixture):
        """Test that all JSON-LD on site has valid JSON syntax."""
        # Test homepage
        homepage = parse_html_fixture(hugo_site / "index.html")
        json_ld_scripts = homepage.find_all('script', attrs={'type': 'application/ld+json'})
        
        for script in json_ld_scripts:
            if script.string:
                try:
                    json.loads(script.string.strip())
                except json.JSONDecodeError as e:
                    pytest.fail(f"Homepage JSON-LD syntax error: {e}")
        
        # Test individual post
        post_soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        json_ld_scripts = post_soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        for script in json_ld_scripts:
            if script.string:
                try:
                    json.loads(script.string.strip())
                except json.JSONDecodeError as e:
                    pytest.fail(f"Post JSON-LD syntax error: {e}")
    
    def test_schema_org_context_consistency(self, hugo_site, get_post_html_fixture, parse_html_fixture):
        """Test that all JSON-LD uses consistent schema.org context."""
        # Test homepage
        homepage = parse_html_fixture(hugo_site / "index.html")
        json_ld_scripts = homepage.find_all('script', attrs={'type': 'application/ld+json'})
        
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                assert data.get('@context') == 'https://schema.org', \
                    "Should use https://schema.org context"
        
        # Test individual post
        post_soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        json_ld_scripts = post_soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                assert data.get('@context') == 'https://schema.org', \
                    "Should use https://schema.org context"
    
    def test_blog_posting_image_handling(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema handles image property correctly."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get BlogPosting schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'BlogPosting':
                    blog_posting_schema = data
                    break
        
        assert blog_posting_schema is not None, "Should have BlogPosting schema"
        
        # If image is present, validate it
        if 'image' in blog_posting_schema:
            image = blog_posting_schema['image']
            assert isinstance(image, str), "Image should be a URL string"
            assert image.startswith('http'), "Image should be absolute URL"
    
    def test_multiple_authors_handling(self, hugo_site, get_post_html_fixture):
        """Test that BlogPosting schema handles multiple authors correctly."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Get BlogPosting schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        blog_posting_schema = None
        for script in json_ld_scripts:
            if script.string:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'BlogPosting':
                    blog_posting_schema = data
                    break
        
        assert blog_posting_schema is not None, "Should have BlogPosting schema"
        
        # Validate author structure
        assert 'author' in blog_posting_schema, "Should have author property"
        authors = blog_posting_schema['author']
        assert isinstance(authors, list), "Authors should be in list format"
        
        # Validate each author
        for author in authors:
            assert author.get('@type') == 'Person', "Each author should be a Person"
            assert 'name' in author, "Each author should have name"
            assert len(author['name'].strip()) > 0, "Author name should not be empty"
    
    def test_all_posts_have_structured_data(self, hugo_site, parse_html_fixture, get_all_posts_fixture):
        """Test that all blog posts have valid structured data."""
        posts = get_all_posts_fixture()
        assert len(posts) > 0, "Should find blog posts"
        
        # Check a few posts to ensure consistency
        posts_to_check = posts[:3]  # Check first 3 posts
        
        for post_path in posts_to_check:
            soup = parse_html_fixture(post_path)
            
            # Skip redirect pages (they have refresh meta tag and minimal content)
            if soup.find('meta', attrs={'http-equiv': 'refresh'}):
                continue
            
            # Should have JSON-LD structured data
            json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
            assert len(json_ld_scripts) > 0, \
                f"Post {post_path} should have JSON-LD structured data"
            
            # Should have at least one BlogPosting schema
            has_blog_posting = False
            for script in json_ld_scripts:
                if script.string:
                    try:
                        data = json.loads(script.string.strip())
                        if data.get('@type') == 'BlogPosting':
                            has_blog_posting = True
                            # Validate required fields
                            assert 'headline' in data, \
                                f"Post {post_path} should have headline"
                            assert 'author' in data, \
                                f"Post {post_path} should have author"
                            assert 'datePublished' in data, \
                                f"Post {post_path} should have datePublished"
                            break
                    except json.JSONDecodeError:
                        pytest.fail(f"Post {post_path} has invalid JSON-LD")
            
            assert has_blog_posting, \
                f"Post {post_path} should have BlogPosting schema"