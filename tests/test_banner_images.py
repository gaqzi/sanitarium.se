"""
Test banner image detection and meta tag generation.

Tests verify:
1. Default banner path resolution (/img/banners/{slug}.png)
2. Custom banner from front matter (if any posts have custom images)
3. Open Graph/Twitter image meta tags include banner images
4. Banner images exist in the static files
5. Specific test for the "which-hat-are-you-wearing" post banner
"""
import pytest
from pathlib import Path
from bs4 import BeautifulSoup


class TestBannerImages:
    """Test suite for banner image functionality."""
    
    def test_default_banner_path_resolution(self, hugo_site, get_post_html_fixture):
        """Test that posts use default banner path based on slug."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Check Open Graph image
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        assert og_image is not None, "Post should have og:image meta tag"
        
        image_url = og_image.get('content', '')
        assert image_url, "og:image should have content"
        
        # Should contain the expected banner path
        assert '/img/banners/2025-07-which-hats-are-you-wearing.png' in image_url, \
            f"Expected banner path in og:image, got: {image_url}"
        
        # Check Twitter image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        assert twitter_image is not None, "Post should have twitter:image meta tag"
        
        twitter_image_url = twitter_image.get('content', '')
        assert twitter_image_url, "twitter:image should have content"
        assert '/img/banners/2025-07-which-hats-are-you-wearing.png' in twitter_image_url, \
            f"Expected banner path in twitter:image, got: {twitter_image_url}"
    
    def test_which_hat_are_you_wearing_banner(self, hugo_site, get_post_html_fixture):
        """Test the specific post 'which-hat-are-you-wearing' has the correct banner."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Verify Open Graph image
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        assert og_image is not None, "which-hat-are-you-wearing post should have og:image"
        
        image_url = og_image.get('content', '')
        assert '/img/banners/2025-07-which-hats-are-you-wearing.png' in image_url, \
            f"which-hat-are-you-wearing should use specific banner, got: {image_url}"
        
        # Verify Twitter image matches
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        assert twitter_image is not None, "which-hat-are-you-wearing post should have twitter:image"
        
        twitter_image_url = twitter_image.get('content', '')
        assert twitter_image_url == image_url, \
            "Open Graph and Twitter images should match"
        
        # Check that og:image dimensions are specified
        og_width = soup.find('meta', attrs={'property': 'og:image:width'})
        og_height = soup.find('meta', attrs={'property': 'og:image:height'})
        
        assert og_width is not None, "Should have og:image:width"
        assert og_height is not None, "Should have og:image:height"
        assert og_width.get('content') == '1200', "og:image:width should be 1200"
        assert og_height.get('content') == '630', "og:image:height should be 630"
    
    def test_banner_images_exist_in_static_files(self, hugo_site):
        """Test that referenced banner images actually exist in static files."""
        # Test the specific banner we know should exist
        project_root = Path(__file__).parent.parent
        banner_path = project_root / "static" / "img" / "banners" / "2025-07-which-hats-are-you-wearing.png"
        
        assert banner_path.exists(), \
            f"Banner image should exist at {banner_path}"
        
        # Verify it's a reasonable file size (not empty)
        assert banner_path.stat().st_size > 1000, \
            f"Banner image should be substantial in size, got {banner_path.stat().st_size} bytes"
    
    def test_multiple_posts_have_banner_images(self, hugo_site, parse_html_fixture, get_all_posts_fixture):
        """Test that multiple posts have banner images defined."""
        posts = get_all_posts_fixture()
        assert len(posts) > 0, "Should find blog posts"
        
        posts_with_banners = 0
        project_root = Path(__file__).parent.parent
        
        # Check first few posts for banner images
        for post_path in posts[:10]:
            soup = parse_html_fixture(post_path)
            
            # Skip redirect pages
            if soup.find('meta', attrs={'http-equiv': 'refresh'}):
                continue
            
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            if og_image:
                image_url = og_image.get('content', '')
                if '/img/banners/' in image_url:
                    posts_with_banners += 1
                    
                    # Extract banner filename from URL
                    banner_filename = image_url.split('/img/banners/')[-1]
                    banner_path = project_root / "static" / "img" / "banners" / banner_filename
                    
                    # Verify the banner file exists
                    assert banner_path.exists(), \
                        f"Banner image should exist at {banner_path} for URL {image_url}"
        
        assert posts_with_banners > 5, \
            f"Should find multiple posts with banners, found {posts_with_banners}"
    
    def test_twitter_card_type_with_banner_images(self, hugo_site, get_post_html_fixture):
        """Test that posts with banner images use summary_large_image Twitter card."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Check Twitter card type
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        assert twitter_card is not None, "Should have twitter:card meta tag"
        
        card_type = twitter_card.get('content', '')
        assert card_type == 'summary_large_image', \
            f"Posts with banner images should use summary_large_image, got: {card_type}"
        
        # Verify there's actually a banner image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        assert twitter_image is not None, "Should have twitter:image if using summary_large_image"
        
        image_url = twitter_image.get('content', '')
        assert '/img/banners/' in image_url, "Should reference a banner image"
    
    def test_banner_image_urls_are_absolute(self, hugo_site, get_post_html_fixture):
        """Test that banner image URLs in meta tags are absolute."""
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        
        # Check Open Graph image URL
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        assert og_image is not None, "Should have og:image"
        
        og_image_url = og_image.get('content', '')
        assert og_image_url.startswith('http'), \
            f"og:image should be absolute URL, got: {og_image_url}"
        
        # Check Twitter image URL
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        assert twitter_image is not None, "Should have twitter:image"
        
        twitter_image_url = twitter_image.get('content', '')
        assert twitter_image_url.startswith('http'), \
            f"twitter:image should be absolute URL, got: {twitter_image_url}"
        
        # Both URLs should be the same
        assert og_image_url == twitter_image_url, \
            "Open Graph and Twitter image URLs should match"
    
    def test_banner_slug_extraction_logic(self, hugo_site, get_post_html_fixture):
        """Test that the banner slug extraction works correctly for different post formats."""
        # Test the main post
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        
        assert og_image is not None, "Should have og:image"
        image_url = og_image.get('content', '')
        
        # The slug should be based on the filename, not the full date path
        assert '2025-07-which-hats-are-you-wearing.png' in image_url, \
            f"Slug should match filename pattern, got: {image_url}"
        
        # Should not contain the full path structure
        assert '/2025/07/12/' not in image_url, \
            "Banner path should not include full date structure"
    
    def test_posts_without_banner_images_graceful_handling(self, hugo_site, parse_html_fixture):
        """Test that posts without banner images still have proper meta tags."""
        # We'll test this by checking if some posts might not have banner images
        # but still have other proper meta tags
        
        # Test homepage which might not have a banner
        homepage = parse_html_fixture(hugo_site / "index.html")
        
        # Should still have proper meta structure
        og_title = homepage.find('meta', attrs={'property': 'og:title'})
        assert og_title is not None, "Homepage should have og:title"
        
        og_type = homepage.find('meta', attrs={'property': 'og:type'})
        assert og_type is not None, "Homepage should have og:type"
        assert og_type.get('content') == 'website', "Homepage og:type should be website"
        
        # If no banner image, should still have basic Twitter card
        twitter_card = homepage.find('meta', attrs={'name': 'twitter:card'})
        assert twitter_card is not None, "Homepage should have twitter:card"
        
        card_type = twitter_card.get('content', '')
        assert card_type in ['summary', 'summary_large_image'], \
            f"Twitter card should be summary or summary_large_image, got: {card_type}"
    
    def test_banner_image_content_type_and_accessibility(self, hugo_site):
        """Test that banner images are proper image files."""
        project_root = Path(__file__).parent.parent
        banners_dir = project_root / "static" / "img" / "banners"
        
        assert banners_dir.exists(), "Banners directory should exist"
        
        banner_files = list(banners_dir.glob("*.png"))
        assert len(banner_files) > 0, "Should find PNG banner files"
        
        # Test specific banner
        test_banner = banners_dir / "2025-07-which-hats-are-you-wearing.png"
        assert test_banner.exists(), "Test banner should exist"
        
        # Check file size is reasonable for an image
        file_size = test_banner.stat().st_size
        assert file_size > 5000, f"Banner should be substantial size, got {file_size} bytes"
        assert file_size < 2_000_000, f"Banner should not be too large, got {file_size} bytes"
        
        # All banner files should follow naming convention
        for banner_file in banner_files:
            filename = banner_file.name
            # Should be a date-prefixed slug
            assert filename.count('-') >= 3, \
                f"Banner filename should follow date-slug pattern: {filename}"
            assert filename.endswith('.png'), \
                f"Banner should be PNG file: {filename}"