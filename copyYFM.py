#!/bin/python3
import os
from pathlib import Path
import multiprocessing as mp
from functools import partial
from pathlib import Path
import re
import yaml
from pprint import PrettyPrinter
import datetime


def pull_YMF(ogFile):
    with open(ogFile, 'r') as og:
        justText = re.search(r'---(.*)---', og.read(), re.DOTALL).group(1).split('\n')
        for line in justText:
            if line.startswith("date-created") or line.startswith('force'):
                justText.remove(line)
    jesus = yaml.safe_load('\n'.join(justText))
    jesus['fileName'] = ogFile.name
    return jesus

def get_read_table(books: list) -> dict:
    readBooks = dict()
   # Use a list comprehension to filter the books by those that have been read
    read_books = [book for book in books if book['time-read']]
    # Loop through the read books and group them by series and fiction/non-fiction
    for book in read_books:
        key = book['Series'] if book['Series'] else "Novels" if book['fiction'] else "Non Fiction"
        readBooks.setdefault(key, []).append(book)
    return readBooks

def get_unread_table(books: list) -> list:
    tabledata = get_table_data_by_key(["Title", "Author", "Series"],
    filter(lambda x: not x["time-read"] and not x["Started"], books))
    
    return make_djot_table(tabledata)



def make_section_of_read(section, header):
        section = sorted(section, key=lambda x: x['number-in-series'] if x['number-in-series'] else 1)
        data = get_table_data_by_key(["Title", "Author", "time-read", "Mood"], section)
        return f"""
        ### {header}\n\n
        |  Title  |  Author  |  Read On  |  Mood  |
        |---------|----------|-----------|--------|
        """ + "\n".join(["|  {}  |".format("   |   ".join(i)) for i in data])


def make_read_table(monster: list) -> str:
    books = get_read_table(monster)
    Novels = books.pop("Novels")
    Nf = books.pop("Non Fiction")
    tables = [make_section_of_read(Novels, "Novels")]
    for header in books.keys():
        tables.append(make_section_of_read(books[header], header))
    tables.append(make_section_of_read(Nf, "Non Fiction"))
    return "\n\n".join(tables)

def get_currently_reading(books: list) -> str:
    currentlyReading = filter(lambda x: x['Started'], 
                       filter(lambda x: not x['time-read'], 
                       filter(lambda x: not x['abandoned'],
                              books)))
    tabledata = get_table_data_by_key(["Title", "Author", "Started"], currentlyReading)
    return make_djot_table(tabledata)

def get_abandoned_books(books : list) -> str:
    abandoned = get_table_data_by_key(
            ["Title", "Author", "abandoned"],
            filter(lambda x: x['abandoned'], books))
    return make_djot_table(abandoned)

def get_table_data_by_key(keys: list, books: dict) -> list:
    returnValue = []
    for book in books:
        dataList = []
        for key in keys:
            if key == "Title":
                dataList.append(f"[{book[key]}](books/{book['fileName']})")
            elif isinstance(book[key], datetime.date):
                dataList.append(book[key].strftime("%b %d, %Y"))
            elif not book[key]:
                dataList.append('')
            else:
                dataList.append(book[key])
        returnValue.append(dataList)
    return returnValue


def make_djot_table(someData: iter) -> str:
    return "\n".join(map(lambda x: "|  " + "  |  ".join(x) + "  |" , someData))




if __name__ == '__main__':
    BooksDir = Path("/home/ellie/vimwiki/Book Files/Books")
    outputDir = Path("/home/ellie/repos/StaticBooks/Booksfm")
    books = [pull_YMF(i) for i in [BooksDir / file for file in os.listdir(BooksDir)]]
    p = PrettyPrinter()
    readBooks = get_read_table(books)
    unReadBooks = get_unread_table(books)
    currentlyReading = get_currently_reading(books)
    print("""
`<LINK href="style.css" rel="stylesheet" type="text/css">`{{=html}}

## Currently Reading

{}

## Read Books

{}

## Unread

|  Title  |  Author  |  Series  |
|---------|----------|----------|
{}

## Abandoned

|  Title  |  Author  |  Stopped reading on  |
|---------|----------|----------------------|
{}
          """.format(
              currentlyReading, 
              make_read_table(books), 
              get_unread_table(books), 
              get_abandoned_books(books)))
