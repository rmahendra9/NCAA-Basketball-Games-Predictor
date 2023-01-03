#
# https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python
#
# Adapted to scrape NCAA D1 Basketball Data from https://www.sports-reference.com/cbb/seasons/2023-school-stats.html

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, urljoin
import time

def get_soup(url):
    session = requests.Session()
    html = session.get(url)
    return bs(html.content, "html.parser")

def get_all_tables(soup):
    return soup.find_all("table")

def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    rows = table.find_all("tr")
    for th in rows[1].find_all("th"):
        headers.append(th.text.strip())

    return headers

def get_table_rows(table):
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
    df = pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")

def main(url):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        headers = headers[1:]
        # get all the rows of the table
        rows = get_table_rows(table)
        rows = rows[1:]
        rows = [row for row in rows if row[0] != "" and row[0] != "Rk"]
        if(url == "https://www.sports-reference.com/cbb/seasons/2023-school-stats.html"):
            ss_table_name = 'NCAA_School_Stats'
        else:
            ss_table_name = 'NCAA_School_Stats_Advanced'
        print(f"[+] Saving {ss_table_name}")
        save_as_csv(ss_table_name, headers, rows)

if __name__ == "__main__":
    main("https://www.sports-reference.com/cbb/seasons/2023-school-stats.html")
    main("https://www.sports-reference.com/cbb/seasons/2023-advanced-school-stats.html")
    df1 = pd.read_csv("NCAA_School_Stats.csv")
    df2 = pd.read_csv("NCAA_School_Stats_Advanced.csv")
    df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
    df2 = df2.loc[:, ~df2.columns.str.contains('^Unnamed')]
    df1.set_index("School",inplace=True)
    df2.set_index("School",inplace=True)
    cols_to_use = df2.columns.difference(df1.columns)
    df3 = pd.merge(df1, df2[cols_to_use], left_index=True, right_index=True)
    df3.to_csv("NCAA_School_Stats_All.csv")
