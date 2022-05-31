#!/bin/sh

echo mkdir
mkdir -v layer_data &&

echo cp
cp -v *.py requirements.txt layer_data &&

echo cd
cd layer_data &&

PYENV_VERSION=3.9.11

echo pip
pip install -r requirements.txt --upgrade --target . &&

unset PYENV_VERSION

echo gfind f
gfind -type f -exec chmod -v 0644 {} \; &&

echo gfind d
gfind -type d -exec chmod -v 0755 {} \; &&

echo zip
zip -r ../layer_data.zip *

echo cd
cd ..

echo rm
rm -rfv layer_data/
