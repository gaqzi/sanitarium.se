.PHONY: build deploy

build: clean
	jekyll build

clean:
	@rm -rf _site

deploy: build
	cd _site && \
		rsync -rvz . sanitarium@cell.sanitarium.se:/srv/www/sanitarium.se/
