#
# https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python
#
# Adapted to scrape NCAA D1 Basketball Data from https://www.sports-reference.com/cbb/seasons/2022-school-stats.html

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    session = requests.Session()
    html = session.get(url)
    return bs(html.content, "html.parser")

def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows

def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")

def main(url):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get all the rows of the table
        rows = get_table_rows(table)
        headers = rows[0]
        rows = rows[1:]
        # get all headers of the table
        # save table as csv file
        table_name = "NCAA-Overall-Team-Stats"
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name, headers, rows)

if __name__ == "__main__":
    import sys
    try:
        url = sys.argv[1]
        if "sports-reference" not in url:
            print("Invalid URL passed, scraper may not work on this website")
            exit(0)
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(0)
    main(url)

