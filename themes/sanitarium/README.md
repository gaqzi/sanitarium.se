# Sanitarium

A clean, minimalist Hugo theme with responsive design and dark mode support.

## Features

- **Responsive Design**: Looks great on all devices, from phones to desktops
- **Dark Mode Support**: Automatically switches between light and dark modes based on system preferences
- **Clean Typography**: Uses system fonts for fast loading and familiar reading experience
- **Code Highlighting**: Beautiful syntax highlighting for code blocks
- **Social Links**: Easy configuration of social media links in the footer
- **Minimal and Fast**: No JavaScript required, loads quickly and efficiently

## Installation

### As a Git Submodule (recommended)

```bash
git submodule add https://github.com/yourusername/sanitarium.git themes/sanitarium
```

### Manual Installation

1. Download the latest release from GitHub
2. Extract the archive into your Hugo site's `themes` directory
3. Rename the extracted folder to `sanitarium`

## Configuration

Add the following to your `hugo.toml` file:

```toml
baseURL = 'https://example.com/'
languageCode = 'en-us'
title = 'Your Site Title'
theme = 'sanitarium'

# Enable syntax highlighting
pygmentsUseClasses = true
pygmentsCodeFences = true

# Enable emojis
enableEmoji = true

# Taxonomies
[taxonomies]
  tag = "tags"
  category = "categories"

# Theme-specific settings
[params]
  # Social media links
  github = "https://github.com/yourusername"
  mastodon = "https://mastodon.social/@yourusername"
  feed = "/index.xml"
  
  # Site settings
  siteName = "Your Site Name"
  description = "Your site description"
  mainSections = ["posts"]
  
  # Theme appearance
  enableCodeHighlighting = true
  footerLogo = "/img/logo.png"
  footerLogoAlt = "Site logo"
  
  # Author information
  author = "Your Name"
```

## Creating Content

### Posts

Create a new post with:

```bash
hugo new content posts/my-post.md
```

The front matter should look like:

```yaml
---
title: "My Post"
subtitle: "Optional subtitle"
date: 2024-05-04T12:00:00-00:00
lastmod: 2024-05-04T14:30:00-00:00
draft: false
author: "Your Name"
tags: ["tag1", "tag2"]
categories: ["Category"]
---
```

## License

This theme is released under the MIT License.

## Credits

- Font Awesome for social media icons
- Hugo community for inspiration