import BookPageMaker
import Book_list_maker
from utils import *
from pprint import PrettyPrinter

books_directory = Path("/home/ellie/vimwiki/Book Files/Books")
outputdir = Path("/home/ellie/repos/StaticBooks/djotsrc/Books")
index_output = Path("/home/ellie/repos/StaticBooks/djotsrc/index.djot")

books = []
for bookFile in books_directory.glob("*"):
    outputFile = outputdir / bookFile.with_suffix('.dj').name
    bookdata = pull_YMF(bookFile)
    print(f"---{bookFile}")
    djot = BookPageMaker.make_book_page(bookdata)
    print(f"\n\n{djot}\n\n\n\n")
    with open(outputFile, 'w') as f:
        try:
            f.write(djot)
        except TypeError:
           print(djot)
    books.append(bookdata)

book_list = Book_list_maker.make_book_list(books)
print(f'\n\n{book_list}')
with open(index_output, 'w') as f:
    f.write(book_list)
