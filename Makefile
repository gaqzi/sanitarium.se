.PHONY: build deploy

build:
	jekyll build

deploy: build
	cd _site && \
		rsync -rvz . sanitarium@cell.sanitarium.se:/srv/www/sanitarium.se/
