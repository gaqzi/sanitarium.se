.PHONY: build deploy
ALL_CSS = css/bootstrap.min.css css/clean-blog.min.css css/syntax.css
ALL_JS = js/bootstrap.js js/clean-blog.js js/jquery.js
ALL_LESS = less/clean-blog.less less/mixins.less less/variables.less

build: clean
	make assets
	jekyll build

clean:
	@rm -rf _site

css/clean-blog.min.css: node_modules $(ALL_LESS)
	grunt less

css/site.css: $(ALL_CSS)
	cat $(ALL_CSS) > $@

js/site.min.js: node_modules $(ALL_JS)
	grunt uglify

node_modules: package.json
	npm install

assets: css/site.css js/site.min.js

deploy: assets build
	cd _site && \
		rsync -rvz \
			--delete-after --delete-excluded \
			. sanitarium@cell.sanitarium.se:/srv/www/sanitarium.se/
