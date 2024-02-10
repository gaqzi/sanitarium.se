.PHONY: build build-with-compose deploy _deploy recreate-banners
ALL_CSS = css/bootstrap.min.css css/clean-blog.min.css css/syntax.css
ALL_JS = js/bootstrap.js js/clean-blog.js js/jquery.js
ALL_LESS = less/clean-blog.less less/mixins.less less/variables.less
SITEMAP = https://sanitarium.se/sitemap.xml

build: clean
	@make assets
	# build twice so if CI generates new banners it's picked up and moved over.
	@make build-with-compose && make build-with-compose

build-with-compose:
	@docker compose -f .devcontainer/docker-compose.yaml -f .devcontainer/docker-compose.ci.yaml up --exit-code-from jekyll

recreate-banners:  ## Shouldn't have to be run very often. Just after major changes in the banners.
	@rm -rf img/banners/*.gen.png && \
		make build && \
		git add img/banners/*.gen.png

clean:
	@rm -rf _site

css/clean-blog.min.css: node_modules/.installed $(ALL_LESS)
	@node_modules/.bin/grunt less

css/site.css: $(ALL_CSS)
	@cat $(ALL_CSS) > $@

js/site.min.js: node_modules/.installed $(ALL_JS)
	@node_modules/.bin/grunt uglify

node_modules/.installed: package.json
	@npm install && \
		touch node_modules/.installed

assets: css/site.css js/site.min.js

ping:
	curl -sSf "https://www.feedburner.com/fb/a/pingSubmit?bloglink=http%3A%2F%2Fsanitarium.se%2F" > /dev/null ; \
	  curl -sSf "https://www.google.com/webmasters/sitemaps/ping?sitemap=$(SITEMAP)" > /dev/null ; \
	  curl -sSf "https://www.bing.com/webmaster/ping.aspx?siteMap=$(SITEMAP)" > /dev/null ; \
	  true

deploy: assets build
	@make _deploy

_deploy:
	@cd _site && \
		rsync -rvz \
			--perms --chmod=Dgo+rx,Fgo+r \
			--delete-after --delete-excluded \
			. sanitarium@cell.sanitarium.se:/srv/www/sanitarium.se/
