#!/bin/sh

PYENV_VERSION=3.9.11

pip install -r requirements.txt --target .

unset PYENV_VERSION

find -type f -exec chmod -v 0644 {} \;
find -type d -exec chmod -v 0755 {} \;
