#!/bin/zsh

python3 copyYFM.py | djot > index.html
git add index.html
git commit -m "Book List Changed"
git push -u origin master
