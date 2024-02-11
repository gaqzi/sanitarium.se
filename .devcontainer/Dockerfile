FROM mcr.microsoft.com/devcontainers/ruby:3.2

COPY Gemfile Gemfile.lock .

RUN /bin/bash -c "source /usr/local/share/nvm/nvm.sh && nvm install 20.11.0"

# So when I run later it will have the resources in the correct place
RUN su vscode -c bundler

CMD make assets && jekyll s --host=0.0.0.0
