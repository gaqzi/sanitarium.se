#!/usr/bin/env python3
"""
Banner Generator for Hugo

This script generates social media banner images for Hugo blog posts by:
1. Checking if Hugo and screenshot services are running (via Docker Compose)
2. Automatically starting Docker Compose if services aren't available
3. Reading a CSV file with post metadata
4. Checking which posts need new banners based on content changes
5. Using a screenshot service to capture HTML templates rendered by Hugo
6. Maintaining a cache of checksums to avoid unnecessary regeneration

The script expects a Docker Compose setup with:
- A Hugo service named 'hugo' serving your site on port 1313
- A ws-screenshot service providing screenshot capabilities on port 3000

If these services aren't running, the script will attempt to start them using
the 'docker-compose up -d' command from the current directory.

Usage:
  python banner_generator.py [options]

Requirements:
  - Python 3.6+
  - Docker and Docker Compose installed
  - A docker-compose.yaml file in the current directory
"""

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class BannerGenerator:
    """Main class for generating banner images for Hugo blog posts."""

    def __init__(self, args):
        """Initialize the banner generator with command line arguments."""
        self.args = args
        self.cache = {}

    def calculate_checksum(self, content):
        """Calculate MD5 checksum of a string."""
        md5 = hashlib.md5()
        md5.update(content.encode('utf-8'))
        return md5.hexdigest()

    def calculate_file_checksum(self, file_path):
        """Calculate MD5 checksum of a file."""
        if not os.path.exists(file_path):
            return None

        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def check_server(self, url, timeout=5):
        """Check if server is running by making a request."""
        try:
            print(f"Checking server at http://{url}/")
            conn = urllib.request.urlopen(f"http://{url}/", timeout=timeout)
            status = conn.getcode()
            print(f"Server responded with HTTP {status}")
            return status == 200
        except (urllib.error.URLError, ConnectionRefusedError) as e:
            print(f"Server check failed: {e}")
            return False

    def check_screenshot_service(self, timeout=2.0):
        """Check if screenshot service is running."""
        try:
            url = self.args.screenshot_url
            req = urllib.request.Request(url)
            req.add_header('Accept-Encoding', 'gzip, deflate')
            req.add_header('User-Agent', 'Mozilla/5.0 Banner Generator')

            with urllib.request.urlopen(req, timeout=timeout) as response:
                status = response.getcode()
                print(f"Screenshot service check: HTTP {status}")
                return status == 200
        except (urllib.error.URLError, ConnectionRefusedError) as e:
            print(f"Screenshot service check failed: {e}")
            return False

    def start_docker_compose(self):
        """Start services using Docker Compose."""
        try:
            print("Starting Docker Compose services...")
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            return self.wait_for_services()
        except Exception as e:
            print(f"Error starting Docker Compose: {e}")
            return False

    def wait_for_services(self):
        """Wait for services to become available after starting Docker Compose."""
        print("Waiting for services to initialize...")

        # Wait for screenshot service
        for attempt in range(15):  # Wait up to 15 seconds
            if self.check_screenshot_service(timeout=1.0):
                print("Screenshot service is now available.")
                break
            print(f"Waiting for screenshot service (attempt {attempt+1}/15)...")
            time.sleep(1)
        else:
            print("Screenshot service did not become available")
            return False

        # Wait for Hugo service
        for attempt in range(15):  # Wait up to 15 seconds
            if self.check_server(self.args.banner_server, timeout=1.0):
                print("Hugo server is now available.")
                break
            print(f"Waiting for Hugo server (attempt {attempt+1}/15)...")
            time.sleep(1)
        else:
            print("Hugo server did not become available")
            return False

        # Both services are now available
        return True

    def check_services(self):
        """Check if required services are available, start them if needed."""
        # Check screenshot service
        if not self.check_screenshot_service():
            print("Screenshot service not available, attempting to start Docker Compose...")
            if not self.start_docker_compose():
                print("Failed to start services via Docker Compose")
                return False
            return True  # Services are now running

        # Check Hugo server
        if not self.check_server(self.args.banner_server):
            print(f"ERROR: Hugo server at {self.args.banner_server} is not responding")
            print("The screenshot service needs Hugo to be running.")
            print("Attempting to start Docker Compose...")
            if not self.start_docker_compose():
                print("Failed to start services via Docker Compose")
                return False
            return True  # Services are now running

        print("All required services are running")
        return True

    def translate_hugo_url(self, url):
        """Translate Hugo URL for Docker network access."""
        # Replace localhost with the container hostname
        if self.args.hugo_container_hostname:
            return url.replace("localhost", self.args.hugo_container_hostname)
        return url

    def load_cache(self):
        """Load the banner cache file or initialize if it doesn't exist."""
        if os.path.exists(self.args.cache_file):
            try:
                with open(self.args.cache_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Cache file {self.args.cache_file} is corrupted. Initializing new cache.")

        return {}

    def save_cache(self):
        """Save the banner cache to a file."""
        with open(self.args.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def capture_screenshot(self, target_url, output_path):
        """Capture a screenshot using the screenshot service."""
        params = {
            'url': target_url,
            'resX': self.args.width,
            'resY': self.args.height,
            'waitTime': self.args.wait_time,
            'isFullPage': 'false',
            'outFormat': 'png'
        }

        query_string = urllib.parse.urlencode(params)
        request_url = f"{self.args.screenshot_url}?{query_string}"

        try:
            print(f"Capturing screenshot of {target_url}")
            print(f"Requesting: {request_url}")

            # Create a request with appropriate headers
            req = urllib.request.Request(request_url)
            req.add_header('Accept-Encoding', 'gzip, deflate')
            req.add_header('User-Agent', 'Mozilla/5.0 Banner Generator')

            # Make the request with a longer timeout
            with urllib.request.urlopen(req, timeout=30) as response:
                # Check the content type to see if we actually got an image
                content_type = response.getheader('Content-Type')
                if content_type and 'image' in content_type:
                    # Ensure output directory exists
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    with open(output_path, 'wb') as out_file:
                        out_file.write(response.read())

                    print(f"Screenshot saved to {output_path}")
                    return True
                else:
                    # We got a response but it's not an image
                    data = response.read()
                    try:
                        text = data.decode('utf-8')
                        print(f"Non-image response received: {text[:200]}...")
                    except:
                        print(f"Non-image response received with content type: {content_type}")
                    return False

            return True
        except urllib.error.URLError as e:
            print(f"URL Error capturing screenshot: {e}")
            print(f"Error details: {e.reason}")
            return False
        except ConnectionResetError as e:
            print(f"Connection reset error: {e}")
            print("This usually indicates a network issue between the script and the screenshot service.")
            return False
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            print(f"Error type: {type(e).__name__}")
            return False

    def process_csv(self):
        """Process the CSV file and generate banners as needed."""
        if not os.path.exists(self.args.csv_path):
            print(f"Error: CSV file {self.args.csv_path} not found.")
            return False

        generation_queue = []

        try:
            with open(self.args.csv_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    # Extract post data
                    path = row.get('path', '')
                    title = row.get('title', '')
                    subtitle = row.get('subtitle', '')
                    date = row.get('date', '')
                    slug = row.get('slug', '')

                    # If slug is not in the CSV, try to extract it from path
                    if not slug and path:
                        # Example: "/posts/my-post/" -> "my-post"
                        slug = path.strip('/').split('/')[-1]

                    if not slug:
                        print(f"Warning: Could not determine slug for post {title}")
                        continue

                    # Clean up the path for URL construction
                    post_path = path.strip('/')
                    if not post_path:
                        # Default to using slug if no path is available
                        post_path = slug

                    # Determine banner path and calculate checksums
                    banner_path = os.path.join(self.args.output_dir, f"{slug}.png")
                    content_checksum = self.calculate_checksum(f"{date}--{title}--{subtitle}")
                    file_checksum = self.calculate_file_checksum(banner_path)

                    # Check if banner needs to be generated
                    cached_data = self.cache.get(banner_path, {})
                    cached_content_checksum = cached_data.get("content_checksum", "")
                    cached_file_checksum = cached_data.get("file_checksum", "")

                    needs_generation = False

                    if not file_checksum:
                        print(f"Banner for '{title}' does not exist, will generate")
                        needs_generation = True
                    elif cached_content_checksum != content_checksum:
                        print(f"Content for '{title}' changed, will regenerate banner")
                        needs_generation = True
                    elif cached_file_checksum != file_checksum:
                        print(f"Banner file for '{title}' was modified, will regenerate")
                        needs_generation = True

                    if needs_generation:
                        generation_queue.append({
                            'slug': slug,
                            'title': title,
                            'path': post_path,
                            'banner_path': banner_path,
                            'content_checksum': content_checksum
                        })

        except Exception as e:
            print(f"Error processing CSV: {e}")
            return False

        # Generate banners for the queue
        for post in generation_queue:
            # Primary URL: use the path from CSV directly with banner.html
            target_url = f"http://{self.args.banner_server}/{post['path']}/banner.html"

            # Translate the URL for Docker network access
            docker_url = self.translate_hugo_url(target_url)
            if docker_url != target_url:
                print(f"Using URL: {target_url} -> {docker_url}")
            else:
                print(f"Using URL: {target_url}")

            success = self.capture_screenshot(
                docker_url,
                post['banner_path']
            )

            if success:
                # Update cache with new checksums
                new_file_checksum = self.calculate_file_checksum(post['banner_path'])
                self.cache[post['banner_path']] = {
                    "content_checksum": post['content_checksum'],
                    "file_checksum": new_file_checksum
                }
                print(f"Successfully generated banner for '{post['title']}'")
            else:
                print(f"Failed to generate banner for '{post['title']}'")

                # If the primary URL fails, try some alternative formats as fallbacks
                fallback_urls = [
                    # Direct slug approach
                    f"http://{self.args.banner_server}/{post['slug']}/banner.html",

                    # With posts prefix
                    f"http://{self.args.banner_server}/posts/{post['slug']}/banner.html",
                ]

                for fallback_url in fallback_urls:
                    translated_url = self.translate_hugo_url(fallback_url)
                    print(f"Trying fallback URL: {fallback_url} -> {translated_url}")

                    success = self.capture_screenshot(
                        translated_url,
                        post['banner_path']
                    )

                    if success:
                        # Update cache with new checksums
                        new_file_checksum = self.calculate_file_checksum(post['banner_path'])
                        self.cache[post['banner_path']] = {
                            "content_checksum": post['content_checksum'],
                            "file_checksum": new_file_checksum
                        }
                        print(f"Successfully generated banner for '{post['title']}' using fallback URL")
                        break

                if not success:
                    print(f"All URL patterns failed for '{post['title']}'")

        return True

    def generate(self):
        """Main generation process."""
        # Load cache
        self.cache = self.load_cache()

        try:
            # Check if services are running
            if not self.check_services():
                return False

            # Process the CSV and generate banners
            if self.process_csv():
                self.save_cache()
                print("Banner generation completed successfully")
                return True
            else:
                print("Banner generation failed")
                return False
        except Exception as e:
            print(f"Error during banner generation: {e}")
            return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate banner images for Hugo posts')

    parser.add_argument('--csv-path', default='public/index.csv',
                        help='Path to Hugo-generated CSV file (default: public/index.csv)')
    parser.add_argument('--output-dir', default='static/img/banners',
                        help='Directory to save banner images (default: static/img/banners)')
    parser.add_argument('--cache-file', default='.banner-cache',
                        help='Path to banner cache file (default: .banner-cache)')
    parser.add_argument('--width', type=int, default=1200,
                        help='Banner width in pixels (default: 1200)')
    parser.add_argument('--height', type=int, default=630,
                        help='Banner height in pixels (default: 630)')
    parser.add_argument('--screenshot-url',
                        default='http://localhost:3000/api/screenshot',
                        help='Screenshot service URL (default: http://localhost:3000/api/screenshot)')
    parser.add_argument('--wait-time', type=int, default=150,
                        help='Wait time in ms for screenshot service (default: 150)')
    parser.add_argument('--banner-server', default='localhost:1313',
                        help='Hugo server URL serving the templates (default: localhost:1313)')
    parser.add_argument('--hugo-container-hostname',
                        default='hugo',
                        help='Hostname for Hugo server within Docker network (default: hugo)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    generator = BannerGenerator(args)
    success = generator.generate()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
