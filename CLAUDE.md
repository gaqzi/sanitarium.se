# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- `hugo server` - Run development server
- `hugo server --disableFastRender` - Run server with live reload
- `hugo` - Build site for production
- `hugo --minify` - Build with minification

## Testing
- Use `hugo` command to build site rather than running the server for testing
- Check generated HTML files in the `public/` directory to verify changes
- Run `grep` on generated files to verify specific implementation details

## Content Creation
- Create new post: `hugo new content/posts/my-post.md`
- Create new page: `hugo new content/pages/my-page.md`

## Project Structure
- Content in Markdown format goes in `content/`
- Templates in `themes/sanitarium/layouts/`
- Static assets in `static/`
- CSS/JS sources in `themes/sanitarium/assets/`

## Style Guidelines
- Use semantic HTML5 elements in templates
- Follow Go template syntax for layouts
- Maintain responsive design principles
- Use Markdown front matter for content metadata
- Organize content with proper section hierarchy
- Test across browsers and device sizes
- Use native CSS nesting with the `&` selector for maintainable CSS
- Prefer concise, nested CSS over verbose repeated selectors

## Hugo Template Structure
The Hugo template system in `themes/sanitarium/layouts/` follows a specific hierarchy. Here's an explanation of each file and directory:

### Base Templates
- `_default/baseof.html` - The main template that defines the overall HTML structure. Modify this to change the site-wide layout.

### Homepage Templates
- `index.html` - Custom homepage template that shows recent posts and site content. Modify this to change the homepage layout.
- `_default/home.html` - Default homepage template used if no index.html exists. Shows all posts from the "posts" section.

### List Templates
- `_default/list.html` - Default template for list pages (sections, taxonomies) with pagination. Modify this for general list page layout changes.
- `posts/list.html` - Custom list template specifically for the posts section. Modify this to change how the posts list page appears.
- `section.html` - Template for section pages without pagination. Used for section pages that don't have a more specific template.
- `taxonomy.html` - Template for taxonomy pages (e.g., /tags/). Similar to section.html but for taxonomies.
- `term.html` - Template for taxonomy term pages (e.g., /tags/hugo/). Similar to section.html but for specific taxonomy terms.

### Single Page Templates
- `_default/single.html` - Default template for single content pages. Modify this for general single page layout changes.
- `_default/post.html` - Template specifically for posts. Currently identical to single.html, but can be customized for posts.
- `_default/page.html` - Template for regular pages (not posts). Simpler than single.html with less metadata.

### Partial Templates
- `partials/` - Directory containing reusable template parts that are included in other templates:
  - `article-summary.html` - Displays a summary of an article for list pages
  - `footer.html` - Site footer
  - `head.html` - HTML head section
  - `header.html` - Site header
  - `menu.html` - Navigation menu
  - `post-meta.html` - Metadata for posts (author, date, etc.)
  - `simple-post-meta.html` - Simplified post metadata
  - `schema.html` - Structured data for SEO
  - `terms.html` - Displays taxonomy terms for a page
  - `head/` - Subdirectory with additional head elements:
    - `css.html` - For including CSS files
    - `js.html` - For including JavaScript files

### Shortcodes
- `shortcodes/` - Directory containing custom shortcodes that can be used in content:
  - `define.html` - Shortcode for defining terms or variables
  - `img.html` - Enhanced image shortcode

### Markdown Rendering
- `_default/_markup/render-heading.html` - Customizes how headings are rendered in markdown content

## Template Modification Guidelines
- To change site-wide structure: Modify `_default/baseof.html`
- To change homepage: Modify `index.html`
- To change how posts are listed: Modify `posts/list.html`
- To change how individual posts appear: Modify `_default/post.html`
- To change how regular pages appear: Modify `_default/page.html`
- To change reusable components: Modify files in the `partials/` directory
- To add custom shortcodes: Add files to the `shortcodes/` directory
- To customize markdown rendering: Add files to the `_default/_markup/` directory

## Template Lookup Order
Hugo uses a specific lookup order to find templates:
1. `/layouts/{section}/{kind}.html` (e.g., `/layouts/posts/single.html`)
2. `/layouts/{type}/{kind}.html` (e.g., `/layouts/post/single.html`)
3. `/layouts/_default/{kind}.html` (e.g., `/layouts/_default/single.html`)

This means more specific templates (by section or type) take precedence over default templates.

## Workflow Guidelines
- When executing a plan with multiple steps, make incremental commits after completing each logical step
- Use descriptive commit messages that clearly explain what was accomplished in each step
- For multi-step processes, include a step number in the commit message (e.g., "Step 1: Create base layout templates")
- Always test changes before committing
- Ensure each commit leaves the codebase in a working state
- NEVER include references to Claude, Claude Code, Anthropic, or AI assistance in commit messages
- Do not add co-author lines or generation tags in commit messages
