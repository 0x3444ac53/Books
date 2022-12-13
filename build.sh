#!/bin/zsh

function make_book_page(){
    local djot_file="$1"
    local book_name="$(basename "$i" ".dj")"
    local output_file="html/books/${book_name}.html"
    printf "    running djot %s %s \n" $djot_file $output_file
    djot $djot_file > $output_file
}

python3 main.py
echo "Generating Index"
djot djotsrc/index.djot > html/index.html
echo "The Books"
for i in djotsrc/Books/*; do 
    make_book_page "$i"
done
git add ./djotsrc ./html
git commit -m "Book List Changed"
git push -u origin master
