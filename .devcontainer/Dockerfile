FROM mcr.microsoft.com/devcontainers/ruby:3.2

COPY Gemfile Gemfile.lock package.json package-lock.json .

RUN /bin/bash -c "source /usr/local/share/nvm/nvm.sh && nvm install 20.11.0"

RUN bundler
RUN /bin/bash -c "npm i"

CMD make assets && jekyll s --host=0.0.0.0
