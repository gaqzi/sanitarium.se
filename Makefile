.PHONY: build deploy
ALL_CSS = css/bootstrap.min.css css/clean-blog.min.css css/syntax.css
ALL_JS = js/bootstrap.js js/clean-blog.js js/jquery.js
ALL_LESS = less/clean-blog.less less/mixins.less less/variables.less
SITEMAP = http://sanitarium.se/sitemap.xml

build: clean
	@make assets
	@bundle exec jekyll build

clean:
	@rm -rf _site

css/clean-blog.min.css: node_modules $(ALL_LESS)
	@node_modules/.bin/grunt less

css/site.css: $(ALL_CSS)
	@cat $(ALL_CSS) > $@

js/site.min.js: node_modules $(ALL_JS)
	@node_modules/.bin/grunt uglify

node_modules: package.json
	@npm install

assets: css/site.css js/site.min.js

ping:
	curl -sSf "http://www.feedburner.com/fb/a/pingSubmit?bloglink=http%3A%2F%2Fsanitarium.se%2F" > /dev/null && \
	  curl -sSf "http://www.google.com/webmasters/sitemaps/ping?sitemap=$(SITEMAP)" > /dev/null && \
	  curl -sSf "http://www.bing.com/webmaster/ping.aspx?siteMap=$(SITEMAP)" > /dev/null 

deploy: assets build
	@cd _site && \
		rsync -rvz \
			--delete-after --delete-excluded \
			. sanitarium@cell.sanitarium.se:/srv/www/sanitarium.se/
