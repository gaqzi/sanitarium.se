# CLAUDE.md

## Commands
- Development: `hugo server` or `hugo server --disableFastRender`
- Production: `hugo` or `hugo --minify`

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

## Template Structure

### Base Templates
- `_default/baseof.html` - Main site structure

### Homepage
- `index.html` - Custom homepage
- `_default/home.html` - Default homepage fallback

### List Templates
- `_default/list.html` - Default for list pages with pagination
- `posts/list.html` - Custom posts list
- `section.html` - For section pages without pagination
- `taxonomy.html` - For taxonomy pages
- `term.html` - For taxonomy term pages

### Single Page Templates
- `_default/single.html` - Default for single content
- `_default/post.html` - For posts
- `_default/page.html` - For regular pages

### Partial Templates
- `partials/` - Reusable components:
  - `article-summary.html` - Article summary for lists
  - `footer.html`, `head.html`, `header.html`
  - `menu.html` - Navigation
  - `post-meta.html`, `simple-post-meta.html`
  - `schema.html` - SEO structured data
  - `terms.html` - Taxonomy terms display
  - `head/css.html`, `head/js.html`

### Shortcodes
- `shortcodes/define.html`, `shortcodes/img.html`

### Markdown Rendering
- `_default/_markup/render-heading.html`

## Modification Guidelines
- Site structure: `_default/baseof.html`
- Homepage: `index.html`
- Post lists: `posts/list.html`
- Individual posts: `_default/post.html`
- Regular pages: `_default/page.html`
- Components: `partials/` directory
- Custom shortcodes: `shortcodes/` directory
- Markdown rendering: `_default/_markup/` directory

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
