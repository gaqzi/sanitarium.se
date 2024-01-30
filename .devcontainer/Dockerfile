FROM mcr.microsoft.com/devcontainers/ruby:2.7

COPY Gemfile Gemfile.lock package.json package-lock.json .

RUN /bin/bash -c "source /usr/local/share/nvm/nvm.sh && nvm install 12.22.10"

RUN bundler
RUN /bin/bash -c "npm i"

CMD ["jekyll", "s", "--host=0.0.0.0"]
