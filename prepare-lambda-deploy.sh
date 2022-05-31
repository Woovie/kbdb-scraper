#!/bin/sh

echo mkdir
mkdir -v deploy &&

echo cp
cp -v *.py deploy &&

echo cd
cd deploy &&

echo gfind f
gfind -type f -exec chmod -v 0644 {} \; &&

echo gfind d
gfind -type d -exec chmod -v 0755 {} \; &&

echo zip
zip -r ../deploy.zip *

echo cd
cd ..

echo rm
rm -rfv deploy/
