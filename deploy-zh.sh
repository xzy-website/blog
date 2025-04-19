#!/bin/bash

rm -rf "_config.butterfly.yml"
rm -rf "_config.yml"

echo "Deleted old files"

cp "config-zh.yml" "_config.yml"
cp "config-butterfly-zh.yml" "_config.butterfly.yml"
cp "gulpfile-zh.js" "gulpfile.js"
cp "links.yml" "source/_data/link.yml"
echo "Set zh success!"
