#!/usr/bin/env python3
"""
Banner Generator for Blog Posts

This script generates social media banner images for blog posts by:
1. Checking that required services (banner server and screenshot service) are running
2. Fetching a CSV file with post metadata from the banner server
3. Checking which posts need new banners based on content changes
4. Using a screenshot service to capture HTML banner templates served by the banner server
5. Maintaining a cache of checksums to avoid unnecessary regeneration

Prerequisites:
- A banner server serving your site with banner templates (typically on port 1313)
- A screenshot service providing screenshot capabilities (typically on port 3000)

The script expects the banner server to:
- Serve a CSV file with post metadata at the root level
- Serve banner templates at /{post-path}/banner.html for each post

Usage:
  python genbanners.py [options]
  python genbanners.py --csv-path public/posts.csv --output-dir static/banners

Requirements:
  - Python 3.6+
  - Running banner server with post templates
  - Running screenshot service (e.g., ws-screenshot)
"""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


class BannerGenerator:
    """Main class for generating banner images for Hugo blog posts.

    It expects to be run from within script/build or something equivalent,
    where everything is running through docker.
    """

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
            print(f"Screenshot service check failed ({url}): {e}")
            return False

    def check_services(self):
        """Check if required services are available, start them if needed."""
        # Check screenshot service
        if not self.check_screenshot_service():
            print("Screenshot service not available")
            return False

        # Check banner server
        if not self.check_server(self.args.banner_server):
            print(f"ERROR: banner server at {self.args.banner_server} is not responding")
            print("The screenshot service needs banner to be running.")
            return False

        print("All required services are running")
        return True

    def normalize_content(self, content):
        """Normalize content string to avoid unnecessary regeneration due to formatting differences."""
        if not content:
            return ""
        # Remove extra whitespace and convert to lowercase
        return ' '.join(content.lower().split())

    def load_cache(self):
        """Load the banner cache file or initialize if it doesn't exist."""
        cache_file_path = self.args.cache_file

        if os.path.exists(cache_file_path):
            try:
                with open(cache_file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Cache file {cache_file_path} is corrupted. Initializing new cache.")
        else:
            print(f"Cache file {cache_file_path} does not exist. Initializing new cache.")

        return {}

    def save_cache(self):
        """Save the banner cache to a file."""
        # Convert cache file path to absolute path if it's not already
        cache_file_path = self.args.cache_file
        if not os.path.isabs(cache_file_path):
            cache_file_path = os.path.abspath(cache_file_path)

        with open(cache_file_path, 'w') as f:
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

                    # Read the response with a timeout to prevent hanging
                    try:
                        # Set a socket timeout for reading the response
                        response.fp.raw._sock.settimeout(60)

                        # Read the response in chunks to avoid memory issues
                        with open(output_path, 'wb') as out_file:
                            chunk_size = 8192  # 8KB chunks
                            while True:
                                chunk = response.read(chunk_size)
                                if not chunk:
                                    break
                                out_file.write(chunk)
                                # Print a dot to show progress
                                print(".", end="", flush=True)

                        print(f"\nScreenshot saved to {output_path}")
                        return True
                    except socket.timeout:
                        print(f"Timeout while reading screenshot response")
                        return False
                    except Exception as e:
                        print(f"Error reading screenshot response: {e}")
                        print(f"Error type: {type(e).__name__}")
                        return False
                else:
                    # We got a response but it's not an image
                    try:
                        # Set a socket timeout for reading the response
                        response.fp.raw._sock.settimeout(10)

                        # Read the response with a timeout
                        data = response.read(8192)  # Read only first 8KB to avoid hanging
                        try:
                            text = data.decode('utf-8')
                            print(f"Non-image response received: {text[:200]}...")
                        except:
                            print(f"Non-image response received with content type: {content_type}")
                        return False
                    except socket.timeout:
                        print(f"Timeout while reading non-image response")
                        return False
                    except Exception as e:
                        print(f"Error reading non-image response: {e}")
                        print(f"Error type: {type(e).__name__}")
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
        # Construct the URL to fetch the CSV from the webserver
        csv_url = f"http://{self.args.banner_server}/{os.path.basename(self.args.csv_path)}"

        generation_queue = []

        try:
            # Fetch the CSV from the webserver
            req = urllib.request.Request(csv_url)
            req.add_header('User-Agent', 'Mozilla/5.0 Banner Generator')

            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    # Check if we got a successful response
                    if response.getcode() == 200:
                        csv_content = response.read().decode('utf-8')
                        reader = csv.DictReader(csv_content.splitlines())

                        # Process each row in the CSV
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
                            pre = f'{date.split('T')[0]}-' if not re.match(r'^\d{4}-\d{2}-(\d{2}-)?', slug) else ''
                            banner_path = os.path.join(self.args.output_dir, f"{pre}{slug}.png")

                            # Normalize content before calculating checksum
                            normalized_date = self.normalize_content(date)
                            normalized_title = self.normalize_content(title)
                            normalized_subtitle = self.normalize_content(subtitle)
                            content_checksum = self.calculate_checksum(
                                f"{normalized_date}--{normalized_title}--{normalized_subtitle}")

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
                                print(
                                    f"Content for '{title}' changed, will regenerate banner ({cached_content_checksum})")
                                needs_generation = True
                            elif cached_file_checksum != file_checksum:
                                print(
                                    f"Banner file for '{title}' was modified, will regenerate ({cached_file_checksum})")
                                needs_generation = True

                            if needs_generation:
                                generation_queue.append({
                                    'slug': slug,
                                    'title': title,
                                    'path': post_path,
                                    'banner_path': banner_path,
                                    'content_checksum': content_checksum
                                })

                        print(f"Preparing to work on {len(generation_queue)} banners")
                    else:
                        print(f"Error: Failed to fetch CSV file. Server returned HTTP {response.getcode()}")
                        return False
            except urllib.error.URLError as e:
                print(f"Error: Failed to fetch CSV file from {csv_url}")
                print(f"URL Error: {e.reason}")
                return False
            except Exception as e:
                print(f"Error: Failed to fetch CSV file from {csv_url}")
                print(f"Error: {e}")
                return False

        except Exception as e:
            print(f"Error processing CSV: {e}")
            return False

        # Generate banners for the queue
        for post in generation_queue:
            # Primary URL: use the path from CSV directly with banner.html
            target_url = f"http://{self.args.banner_server}/{post['path']}/banner.html"

            success = self.capture_screenshot(target_url, post['banner_path'])

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
                return False

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
    parser.add_argument('--start-delay', type=float, default=0,
                        help='Sleeps this many seconds before starting the work, to allow dependencies to start (default: 0)')
    try:
        return parser.parse_args()
    except SystemExit as e:
        print(f"argparse failed with exit code: {e.code}")
        print("This usually means invalid arguments or --help was called")
        raise


def main():
    """Main function."""
    args = parse_args()

    if args.start_delay:
        print(f'Waiting {args.start_delay} seconds...')
        time.sleep(args.start_delay)

    generator = BannerGenerator(args)
    success = generator.generate()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
