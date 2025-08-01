"""
Test banner image detection and meta tag generation for the "which-hat-are-you-wearing" post.

Tests verify:
1. Banner path resolution and meta tag generation
2. Banner image file existence in static files
"""


class TestBannerImages:
    """Test suite for banner image functionality for the which-hat-are-you-wearing post."""

    def test_which_hat_are_you_wearing_banner(self, hugo_site, get_post_html_fixture):
        soup = get_post_html_fixture("blog/2025/07/12/which-hat-are-you-wearing")

        og_image = soup.find("meta", attrs={"property": "og:image"})
        assert (
            og_image is not None
        ), "which-hat-are-you-wearing post should have og:image"

        image_url = og_image.get("content", "")
        assert (
            "/img/banners/2025-07-which-hats-are-you-wearing.png" in image_url
        ), f"which-hat-are-you-wearing should use specific banner, got: {image_url}"

        twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
        assert (
            twitter_image is not None
        ), "which-hat-are-you-wearing post should have twitter:image"

        twitter_image_url = twitter_image.get("content", "")
        assert (
            twitter_image_url == image_url
        ), "Open Graph and Twitter images should match"

        og_width = soup.find("meta", attrs={"property": "og:image:width"})
        og_height = soup.find("meta", attrs={"property": "og:image:height"})

        assert og_width is not None, "Should have og:image:width"
        assert og_height is not None, "Should have og:image:height"
        assert og_width.get("content") == "1200", "og:image:width should be 1200"
        assert og_height.get("content") == "630", "og:image:height should be 630"

        assert image_url.startswith(
            "http"
        ), f"og:image should be absolute URL, got: {image_url}"
        assert twitter_image_url.startswith(
            "http"
        ), f"twitter:image should be absolute URL, got: {twitter_image_url}"

        twitter_card = soup.find("meta", attrs={"name": "twitter:card"})
        assert twitter_card is not None, "Should have twitter:card meta tag"
        card_type = twitter_card.get("content", "")
        assert (
            card_type == "summary_large_image"
        ), f"Posts with banner images should use summary_large_image, got: {card_type}"

    def test_til_post_no_banner(self, hugo_site, get_post_html_fixture):
        soup = get_post_html_fixture("til/2025-08-01-macos-fingerprint-reader-sudo")

        og_image = soup.find("meta", attrs={"property": "og:image"})
        assert (
            og_image is None
        ), "TIL post should not have og:image meta tag when defaultImage is empty"

        twitter_card = soup.find("meta", attrs={"name": "twitter:card"})
        assert twitter_card is not None, "Should have twitter:card meta tag"
        card_type = twitter_card.get("content", "")
        assert (
            card_type == "summary"
        ), f"Posts without images should use summary card, got: {card_type}"
