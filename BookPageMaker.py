from utils import *
from datetime import datetime, timedelta, date, time

def make_book_page(bookdata):
    template = """

`<LINK href="../style.css" rel="stylesheet" type="text/css">`{{=html}}

# {}
## by {}

{}
""" # title, author, table

    headerdata = get_table_data_by_key(["Title", "Author"], [bookdata], make_link=False)[0]
    table_rows = []
    get_delta = ''
    if bookdata["Series"]:
        table_rows.append("Series")
        table_rows.append("number-in-series")
    if bookdata['Started']:
        table_rows.append("Started")
    if bookdata['time-read']:
        table_rows.append("time-read")
        get_delta = 'time-read'
    if bookdata['abandoned']:
        table_rows.append("abandoned")
        get_delta = 'abandoned'
    table_data = get_table_data_by_key(table_rows, [bookdata])
    if get_delta:
        table_rows.append("Time Spent" if "time-read" in table_rows else "Time Wasted")
        started_on = bookdata['Started']
        try:
            finished_on = bookdata[get_delta].date()
        except AttributeError:
            finished_on = bookdata[get_delta]
        delta = finished_on - started_on
        table_data[0].append(f"{delta.days} Days")
    print(f"{headerdata=}")
    print(f"{table_data=}")
    return template.format(
            headerdata[0],
            headerdata[1],
            make_djot_table(zip(table_rows, table_data[0])))
