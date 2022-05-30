#!/bin/sh

mkdir -v deploy &&

cp -v *.py requirements.txt deploy &&

cd deploy &&

mv lambda_scrape.py lambda_function.py &&

PYENV_VERSION=3.9.11

pip install -r requirements.txt --upgrade --target . &&

unset PYENV_VERSION

gfind -type f -exec chmod -v 0644 {} \; &&
gfind -type d -exec chmod -v 0755 {} \; &&

tar -czvf ../deploy.tar.gz *
