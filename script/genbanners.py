#!/usr/bin/env python3
"""
Banner Generator for Hugo

This script generates social media banner images for Hugo blog posts by:
1. Reading a CSV file with post metadata
2. Checking which posts need new banners based on content changes
3. Using a screenshot service to capture HTML templates rendered by Hugo
4. Maintaining a cache of checksums to avoid unnecessary regeneration

Usage:
  python banner_generator.py [options]

Requirements:
  - Python 3.6+
  - Docker for automatic screenshot service (optional)
  - Hugo for local development server (optional)
"""

import argparse
import contextlib
import csv
import hashlib
import json
import os
import platform
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
        self.hugo_process = None
        self.screenshot_container_id = None
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
        """Check if server is running by making a HEAD request."""
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
        """Check if screenshot service is running with a short timeout."""
        try:
            url = self.args.screenshot_url
            # Create a request object to add headers
            req = urllib.request.Request(url)
            # Add the Accept-Encoding header for compression
            req.add_header('Accept-Encoding', 'gzip, deflate')
            req.add_header('User-Agent', 'Mozilla/5.0 Banner Generator')

            # Open with the custom request
            conn = urllib.request.urlopen(req, timeout=timeout)
            status = conn.getcode()
            print(f"Screenshot service check: HTTP {status}")
            return status == 200
        except (urllib.error.URLError, ConnectionRefusedError) as e:
            print(f"Screenshot service check failed: {e}")
            # Check if Docker container is still running
            if self.screenshot_container_id:
                try:
                    inspect_cmd = ["docker", "inspect", "--format", "{{.State.Status}}", self.screenshot_container_id]
                    result = subprocess.run(inspect_cmd, check=True, stdout=subprocess.PIPE, text=True, timeout=5)
                    status = result.stdout.strip()
                    print(f"Container status: {status}")

                    # Get container logs
                    logs_cmd = ["docker", "logs", "--tail", "20", self.screenshot_container_id]
                    result = subprocess.run(logs_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=5)
                    logs = result.stdout.strip()
                    print(f"Container logs:\n{logs}")
                except Exception as debug_e:
                    print(f"Error getting container debug info: {debug_e}")
            return False

    def wait_for_server(self, url, max_attempts=10, initial_wait=0.5):
        """Wait for server to become available with exponential backoff."""
        wait_time = initial_wait
        for attempt in range(max_attempts):
            if self.check_server(url):
                return True
            print(f"Waiting for server at {url} (attempt {attempt+1}/{max_attempts})...")
            time.sleep(wait_time)
            wait_time *= 1.5  # Exponential backoff

        return False

    def wait_for_screenshot_service(self, max_attempts=10, initial_wait=0.5):
        """Wait for screenshot service with exponential backoff."""
        wait_time = initial_wait
        for attempt in range(max_attempts):
            if self.check_screenshot_service():
                return True
            print(f"Waiting for screenshot service (attempt {attempt+1}/{max_attempts})...")
            time.sleep(wait_time)
            wait_time *= 1.5

        return False

    def check_services(self):
        """Check if required services are running."""
        # Check Hugo server
        print("\n=== Checking Hugo Server ===")
        if not self.check_server(self.args.banner_server):
            print(f"ERROR: Hugo server at {self.args.banner_server} is not responding")
            print("The screenshot service needs Hugo to be running")
            print("Please make sure Hugo is running via docker-compose")
            return False
        print(f"✓ Hugo server is running at {self.args.banner_server}")

        # Check screenshot service
        print("\n=== Checking Screenshot Service ===")
        if not self.check_screenshot_service():
            print(f"ERROR: Screenshot service at {self.args.screenshot_url} is not responding")
            print("Please make sure the ws-screenshot container is running via docker-compose")
            return False
        print(f"✓ Screenshot service is running at {self.args.screenshot_url}")

        return True

    def translate_hugo_url(self, url):
        """Translate Hugo URL for Docker network access."""
        # Replace localhost with the container hostname
        if self.args.hugo_container_hostname:
            return url.replace("localhost", self.args.hugo_container_hostname)
        return url

    def is_docker_available(self):
        """Check if Docker is available on the system."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def start_screenshot_container(self):
        """Start a Docker container for the screenshot service."""
        # Try a different Docker image - elestio/puppeteer which is more stable
        if platform.machine() in ('arm64', 'aarch64', 'armv8l'):
            image = "elestio/puppeteer:latest"
        else:
            image = "elestio/puppeteer:latest"

        port = "3000"

        try:
            print(f"Starting screenshot container: {image}")

            # Determine network configuration based on args or auto-detect
            host_option = []

            if self.args.docker_network == 'auto':
                # Auto-detect based on platform
                if sys.platform == 'darwin':  # macOS uses host.docker.internal
                    host_option = ["--add-host", "host.docker.internal:host-gateway"]
                elif sys.platform == 'linux':  # Linux needs network access
                    host_option = ["--network", "host"]
            elif self.args.docker_network == 'host':
                host_option = ["--network", "host"]
            elif self.args.docker_network == 'bridge':
                # Bridge is default, no special options needed for network
                pass
            elif self.args.docker_network == 'none':
                host_option = ["--network", "none"]

            # If explicit hostname provided, add it
            if self.args.docker_host_name:
                host_option = ["--add-host", f"{self.args.docker_host_name}:host-gateway"]

            # Create a simple HTTP server using Node.js
            entrypoint_cmd = ["--entrypoint", "/bin/sh"]

            run_cmd = [
                "docker", "run",
                "-d",  # Detached mode
            ]

            # For host network, don't specify port mapping
            if self.args.docker_network != 'host' and '--network' not in ' '.join(host_option):
                run_cmd.extend(["-p", f"{port}:{port}"])  # Port mapping

            run_cmd.extend([
                "--rm",  # Remove container when stopped
            ])

            # Add host options if available
            if host_option:
                run_cmd.extend(host_option)

            # Add the entrypoint override
            run_cmd.extend(entrypoint_cmd)

            # Add the image name
            run_cmd.append(image)

            # Add the command to create a simple HTTP server
            run_cmd.extend(["-c", f"""
                echo 'Starting simple screenshot service...'
                mkdir -p /tmp/server
                cat > /tmp/server/server.js << 'EOF'
                const http = require('http');
                const { execSync } = require('child_process');
                const url = require('url');
                const fs = require('fs');
                const path = require('path');
                
                const server = http.createServer((req, res) => {{
                    console.log(`Received request: ${{req.url}}`);
                    
                    if (req.url.startsWith('/api/screenshot')) {{
                        // Parse query parameters
                        const queryParams = url.parse(req.url, true).query;
                        const targetUrl = queryParams.url;
                        const width = queryParams.resX || 1200;
                        const height = queryParams.resY || 630;
                        const waitTime = queryParams.waitTime || 100;
                        
                        if (!targetUrl) {{
                            res.writeHead(400, {{ 'Content-Type': 'text/plain' }});
                            res.end('Missing url parameter');
                            return;
                        }}
                        
                        console.log(`Taking screenshot of ${{targetUrl}} at ${{width}}x${{height}}`);
                        
                        // Generate a unique output filename
                        const outputFile = `/tmp/screenshot-${{Date.now()}}.png`;
                        
                        try {{
                            // Use npx for local version of puppeteer
                            const script = `
                            const puppeteer = require('puppeteer');
                            
                            (async () => {{
                              const browser = await puppeteer.launch({{
                                headless: 'new',
                                args: ['--no-sandbox', '--disable-setuid-sandbox']
                              }});
                              const page = await browser.newPage();
                              await page.setViewport({{ width: ${{width}}, height: ${{height}} }});
                              await page.goto('${{targetUrl}}', {{ waitUntil: 'networkidle0' }});
                              await page.screenshot({{ path: '${{outputFile}}' }});
                              await browser.close();
                              console.log('Screenshot saved to ${{outputFile}}');
                            }})();
                            `;
                            
                            // Write the script to a file
                            fs.writeFileSync('/tmp/screenshot.js', script);
                            
                            // Execute the script
                            execSync('node /tmp/screenshot.js', {{ timeout: 30000 }});
                            
                            // Read the screenshot file
                            const screenshotData = fs.readFileSync(outputFile);
                            
                            // Respond with the screenshot
                            res.writeHead(200, {{ 'Content-Type': 'image/png' }});
                            res.end(screenshotData);
                            
                            // Delete the file
                            fs.unlinkSync(outputFile);
                        }} catch (error) {{
                            console.error(`Error taking screenshot: ${{error.message}}`);
                            res.writeHead(500, {{ 'Content-Type': 'text/plain' }});
                            res.end(`Error taking screenshot: ${{error.message}}`);
                        }}
                    }} else {{
                        // Root path
                        res.writeHead(200, {{ 'Content-Type': 'text/plain' }});
                        res.end('Screenshot service is running');
                    }}
                }});
                
                const PORT = {port};
                server.listen(PORT, '0.0.0.0', () => {{
                    console.log(`Screenshot server listening on port ${{PORT}}`);
                }});
                EOF
                cd /tmp/server
                node server.js
            """])

            print(f"Running docker command: {' '.join(run_cmd)}")
            result = subprocess.run(run_cmd, check=True, stdout=subprocess.PIPE, text=True)
            container_id = result.stdout.strip()
            print(f"Started screenshot container: {container_id[:12]}")

            # Give the Node.js server a moment to start
            time.sleep(2)

            return container_id
        except subprocess.CalledProcessError as e:
            print(f"Error starting Docker container: {e}")
            return None

    def stop_docker_container(self):
        """Stop a Docker container."""
        if not self.screenshot_container_id:
            return

        try:
            stop_cmd = ["docker", "stop", self.screenshot_container_id]
            subprocess.run(stop_cmd, check=True, stdout=subprocess.PIPE)
            print(f"Stopped screenshot container: {self.screenshot_container_id[:12]}")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping Docker container: {e}")

    def start_hugo_server(self):
        """Start Hugo server as a subprocess."""
        try:
            print(f"Starting Hugo server: {self.args.hugo_binary} server {self.args.hugo_args}")
            process = subprocess.Popen(
                [self.args.hugo_binary, "server"] + (self.args.hugo_args.split() if self.args.hugo_args else []),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return process
        except Exception as e:
            print(f"Error starting Hugo server: {e}")
            return None

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
        # First check if the target URL is accessible
        try:
            print(f"Checking if target URL exists: {target_url}")
            # Create a request object to add headers
            req = urllib.request.Request(target_url)
            req.add_header('Accept-Encoding', 'gzip, deflate')
            req.add_header('User-Agent', 'Mozilla/5.0 Banner Generator')

            # Try to open the URL directly (this will fail if containers can't talk to each other)
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    status = response.getcode()
                    print(f"Target URL responded with HTTP {status}")
                    if status == 404:
                        print("WARNING: Page not found at the target URL")
                        print("Check if banner.html template exists at this location")
            except Exception as e:
                print(f"Could not directly check target URL: {e}")
                print("This is expected if checking container URLs from host")

        except Exception as e:
            print(f"Error checking target URL: {e}")

        # Proceed with screenshot capture
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
            print("If using Docker, make sure the container can access your Hugo server.")
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

                    # Path with /index/banner.html
                    f"http://{self.args.banner_server}/{post['path']}/index/banner.html",
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

    def run_test_mode(self):
        """Run a simple test to isolate Docker/Hugo connectivity issues."""
        print("\n=== Running in Test Mode ===")

        # Create a simple HTML file
        test_html = """<!DOCTYPE html>
<html>
<head>
    <title>Banner Test</title>
    <style>
        body {
            background-color: #1a1a1a;
            color: white;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .content {
            text-align: center;
            max-width: 800px;
        }
        h1 {
            font-size: 48px;
            margin-bottom: 10px;
        }
        p {
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Banner Test</h1>
        <p>This is a test banner for debugging purposes.</p>
        <p>Generated: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
</body>
</html>
"""
        # Create a temporary directory to serve the HTML file
        import tempfile
        import http.server
        import socketserver
        import threading

        with tempfile.TemporaryDirectory() as temp_dir:
            # Write the HTML file
            test_file_path = os.path.join(temp_dir, "test.html")
            with open(test_file_path, "w") as f:
                f.write(test_html)

            print(f"Created test HTML file at {test_file_path}")

            # Start a simple HTTP server in a separate thread
            port = 8000
            handler = http.server.SimpleHTTPRequestHandler

            # Change to the temporary directory for serving files
            os.chdir(temp_dir)

            httpd = socketserver.TCPServer(("", port), handler)
            print(f"Starting test HTTP server on port {port}")

            # Start the server in a separate thread
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            try:
                # Test if the server is running
                print("Testing local HTTP server...")
                test_url = f"http://localhost:{port}/test.html"
                try:
                    with urllib.request.urlopen(test_url, timeout=5) as response:
                        print(f"Local server test: {response.status} {response.reason}")
                except Exception as e:
                    print(f"Error testing local server: {e}")

                # Try to capture a screenshot
                print("\nAttempting to capture screenshot...")
                output_path = os.path.join(self.args.output_dir, "test_banner.png")

                # Use the screenshot service context manager
                with self.screenshot_service() as screenshot_url:
                    # Construct the target URL for the test HTML
                    if self.screenshot_container_id:
                        # Use appropriate URL for Docker
                        target_url = self.translate_hugo_url(test_url)
                        print(f"Using translated URL for Docker: {target_url}")
                    else:
                        target_url = test_url

                    # Capture the screenshot
                    success = self.capture_screenshot(target_url, output_path)

                    if success:
                        print(f"Success! Test banner saved to {output_path}")
                    else:
                        print("Failed to generate test banner")

            finally:
                # Shut down the server
                print("Shutting down test HTTP server")
                httpd.shutdown()
                httpd.server_close()
                server_thread.join(timeout=5)

        return True

    @contextlib.contextmanager
    def screenshot_service(self):
        """Context manager that ensures screenshot service is available."""
        # Check if Hugo server is running first - this is critical
        print("\n=== Checking Hugo Server ===")
        if not self.check_server(self.args.banner_server):
            print(f"ERROR: Hugo server at {self.args.banner_server} is not responding")
            print("The ws-screenshot service needs Hugo to be running to capture banners.")
            print("Please start Hugo server with: hugo server")
            raise RuntimeError(f"Hugo server not running at {self.args.banner_server}")
        else:
            print(f"✓ Hugo server is running at {self.args.banner_server}")

        # Check if service is already running
        if self.check_screenshot_service():
            print("Screenshot service is already running")
            yield self.args.screenshot_url
            return

        # Make sure Docker is available
        if not self.is_docker_available():
            print("Warning: Docker not available, cannot auto-start screenshot service")
            yield self.args.screenshot_url
            return

        # Start container if needed
        self.screenshot_container_id = self.start_screenshot_container()
        try:
            if not self.screenshot_container_id:
                print("Failed to start screenshot container")
                yield self.args.screenshot_url
                return

            # Wait for the service to be ready
            print("Waiting for screenshot service to initialize...")
            max_attempts = 10
            for attempt in range(max_attempts):
                if self.check_screenshot_service():
                    print(f"Screenshot service is ready after {attempt+1} attempts")
                    yield self.args.screenshot_url
                    return
                print(f"Waiting for screenshot service (attempt {attempt+1}/{max_attempts})...")
                time.sleep(1)  # Wait 1 second between checks

            # If we got here, the service didn't initialize properly
            print("\n=== Screenshot Service Troubleshooting ===")
            print("Screenshot service did not start properly")
            print("Testing URL translation to diagnose networking issues:")
            print(f"Original Hugo URL: http://{self.args.banner_server}")
            translated_url = self.translate_hugo_url(f"http://{self.args.banner_server}")
            print(f"Translated URL for Docker: {translated_url}")

            # Check container network settings
            print("\nContainer network settings:")
            net_cmd = ["docker", "inspect", "--format", "{{.NetworkSettings.Networks}}", self.screenshot_container_id]
            subprocess.run(net_cmd, check=False, timeout=5)

            raise RuntimeError("Screenshot service did not start properly")
        finally:
            if self.screenshot_container_id:
                self.stop_docker_container()
                self.screenshot_container_id = None

    @contextlib.contextmanager
    def hugo_server(self):
        """Context manager that ensures Hugo server is running."""
        # Check if server is already running
        if self.check_server(self.args.banner_server):
            print(f"Hugo server is already running at {self.args.banner_server}")
            yield self.args.banner_server
            return

        # Start Hugo server if needed
        if self.args.auto_start_hugo:
            self.hugo_process = self.start_hugo_server()
            try:
                if self.wait_for_server(self.args.banner_server):
                    yield self.args.banner_server
                else:
                    raise RuntimeError(f"Could not connect to Hugo server at {self.args.banner_server}")
            finally:
                if self.hugo_process:
                    print("Shutting down Hugo server")
                    self.hugo_process.terminate()
                    self.hugo_process = None
        else:
            # If auto-start is disabled, just yield the server URL
            yield self.args.banner_server

    def generate(self):
        """Main generation process."""
        # Load cache
        self.cache = self.load_cache()

        try:
            # Check if services are running
            if not self.check_services():
                return False

            # Special test mode
            if self.args.test_mode:
                return self.run_test_mode()

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
    parser.add_argument('--test-mode', action='store_true',
                        help='Run in test mode with a simple HTML file instead of Hugo')
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
