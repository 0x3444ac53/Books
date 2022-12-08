import BookPageMaker
import Book_list_maker
import BookPageMaker
from utils import *
from pprint import PrettyPrinter

books_directory = Path("/home/ellie/vimwiki/Book Files/Books")
outputdir = Path("/home/ellie/repos/StaticBooks/djotsrc/Books")
index_output = Path("/home/ellie/repos/StaticBooks/djotsrc/index.djot")

books = []
for bookFile in books_directory.glob("*"):
    outputFile = outputdir / bookFile.with_suffix('.dj').name
    bookdata = pull_YMF(bookFile)
    djot = BookPageMaker.make_book_page(bookdata)
    with open(outputFile, 'w') as f:
        f.write(djot)
    books.append(bookdata)

book_list = Book_list_maker.make_book_list(books)
with open(index_output, 'w') as f:
    f.write(book_list)
