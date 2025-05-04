# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- `hugo server` - Run development server
- `hugo server --disableFastRender` - Run server with live reload
- `hugo` - Build site for production
- `hugo --minify` - Build with minification

## Testing
- Use `hugo` command to build site rather than running the server for testing SEO and functionality
- Check generated HTML files in the `public/` directory to verify changes
- Run `grep` on generated files to verify specific implementation details

## Content Creation
- Create new post: `hugo new content/posts/my-post.md`
- Create new page: `hugo new content/pages/my-page.md`

## Project Structure
- Content in Markdown format goes in `content/`
- Templates in `layouts/`
- Static assets in `static/`
- CSS/JS sources in `assets/`

## Style Guidelines
- Use semantic HTML5 elements in templates
- Follow Go template syntax for layouts
- Maintain responsive design principles
- Use Markdown front matter for content metadata
- Organize content with proper section hierarchy
- Test across browsers and device sizes
- Use native CSS nesting with the `&` selector for maintainable CSS
- Prefer concise, nested CSS over verbose repeated selectors

## Workflow Guidelines
- When executing a plan with multiple steps, make incremental commits after completing each logical step
- Use descriptive commit messages that clearly explain what was accomplished in each step
- For multi-step processes, include a step number in the commit message (e.g., "Step 1: Create base layout templates")
- Always test changes before committing
- Ensure each commit leaves the codebase in a working state
- NEVER include references to Claude, Claude Code, Anthropic, or AI assistance in commit messages
- Do not add co-author lines or generation tags in commit messages