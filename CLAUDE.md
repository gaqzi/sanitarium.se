# CLAUDE.md

## Commands
- Development: `hugo server` or `hugo server --disableFastRender`
- Production: `hugo` or `hugo --minify`

## Scripts
- **Setup**: `script/bootstrap` - Install tools and dependencies
- **Build**: `script/build` - Run linting checks then build with Docker Compose
- **Linting**: `script/lint` - Validate project consistency (runs silently unless errors found)
  - Validates `data/tags.yaml` against `schemas/tags-schema.yaml`
  - Ensures all content tags are declared in `data/tags.yaml`
- **Tag Analysis**: `script/all-tags.py` - Extract and count all tags from markdown content

## Testing
- Build with `hugo`, check files in `public/` directory

## Content
- New post: `hugo new content/posts/my-post.md`
- New page: `hugo new content/pages/my-page.md`

## Structure
- Content: `content/` (Markdown)
- Templates: `themes/sanitarium/layouts/`
- Static assets: `static/`
- CSS/JS sources: `themes/sanitarium/assets/`

## Style Guidelines
- Use semantic HTML5 elements
- Follow Go template syntax
- Maintain responsive design
- Use proper Markdown front matter
- Organize with section hierarchy
- Cross-browser/device testing
- Use native CSS nesting with `&`
- Support dark/light themes:
  - Leverage browser standard colors (like `CanvasText`) to minimize custom CSS
  - Define theme variables in `:root` with light/dark pairs
  - Use `prefers-color-scheme` media queries for automatic theme switching
  - Only define custom colors when browser defaults aren't sufficient
  - Test all color combinations for sufficient contrast in both themes
  - For SVGs and icons, use filters rather than duplicate assets

## Template Structure

### Base Templates
- `_default/baseof.html` - Main site structure

### Homepage
- `_default/home.html` - Default homepage fallback

### List Templates
- `_default/list.html` - Default for list pages with pagination

### Section Templates
- `authors/single.html` - Author profile pages

### Single Page Templates
- `_default/single.html` - Individual posts and pages
- `_default/single.banner.html` - Banner variant for posts

### Partial Templates
- `partials/` - Reusable components:
  - `post-in-listing.html` - Article display in list views
  - `footer.html`, `head.html`, `header.html`
  - `menu.html` - Navigation
  - `post-meta.html` - Post metadata display
  - `schema.html` - SEO structured data
  - `terms.html` - Taxonomy terms display
  - `title-with-subtitle.html` - Page title formatting
  - `head/` - Head section sub-partials:
    - `css.html` - Stylesheet loading
    - `meta-basic.html` - Basic HTML meta tags
    - `meta-social.html` - Social media meta tags
    - `banner-image.html` - Banner image detection
    - `feeds.html` - RSS feed links

### Shortcodes
- `shortcodes/define.html`, `shortcodes/img.html`

### Markdown Rendering
- `_default/_markup/render-heading.html` - Custom heading renderer
- `_markup/render-codeblock-mermaid.html` - Mermaid diagram support

### Data Templates
- `index.post-data.csv` - Post metadata export

## Modification Guidelines
- Site structure: `_default/baseof.html`
- Individual posts/pages: `_default/single.html`
- Author pages: `authors/single.html`
- List pages: `_default/list.html`
- Components: `partials/` directory
- Custom shortcodes: `shortcodes/` directory
- Markdown rendering: `_default/_markup/` and `_markup/` directories

## Template Lookup Order
1. `/layouts/{section}/{kind}.html`
2. `/layouts/{type}/{kind}.html`
3. `/layouts/_default/{kind}.html`

## Workflow Guidelines
- Make incremental commits after each logical step
- Use descriptive commit messages
- Include step numbers for multi-step processes
- Test before committing
- Each commit should leave code in working state
- Keep commit messages focused on technical details
