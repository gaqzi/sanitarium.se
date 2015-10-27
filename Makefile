.PHONY: build deploy
ALL_CSS_FILES = css/bootstrap.min.css css/clean-blog.min.css css/syntax.css

build: clean
	jekyll build

clean:
	@rm -rf _site

css/site.css: $(ALL_CSS_FILES)
	cat $(ALL_CSS_FILES) > $@

node_modules: package.json
	npm install

assets-compress: node_modules
	grunt

assets-concat: css/site.css

assets: assets-compress assets-concat

deploy: assets build
	cd _site && \
		rsync -rvz . sanitarium@cell.sanitarium.se:/srv/www/sanitarium.se/
