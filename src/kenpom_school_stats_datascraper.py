#
# https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python
#
# Adapted to scrape NCAA D1 Basketball Data from https://barttorvik.com/trank.php#

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs, NavigableString

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
                if len(td.contents) > 0:
                    if isinstance(td.contents[0], NavigableString):
                        text = td.contents[0]
                    else:
                        text = td.contents[0].contents[0]
                    cells.append(text)
                else:
                    cells.append('')
        rows.append(cells)
    return rows

def save_as_csv(table_name, headers, rows):
    df = pd.DataFrame(rows, columns=headers)
    df = df.drop("Rk", axis=1)
    df.set_index("Team")
    df.to_csv(f"{table_name}.csv")

def main(url, year):
    # get the soup
    soup = bs(open(url).read(), 'html.parser')
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = ['Rk', 'Team', 'Conf', 'W-L', 'AdjEM', 'AdjO', '', 'AdjD', '', 'AdjT', '', 'Luck', '', 'SOS (AdjEM)', '', 'SOS (OppO)', '', 'SOS (OppD)', '', 'NCSOS (AdjEM)', '']
        # get all the rows of the table
        rows = get_table_rows(table)
        rows = rows[1:]
        rows = [row for row in rows if row[0] != "" and row[0] != "Rk"]
        ss_table_name = 'Tempo_Free_Statistics_' + year
        print(f"[+] Saving {ss_table_name}")
        save_as_csv(ss_table_name, headers, rows)
    


if __name__ == "__main__":
    main(r"C:\\Users\\theeliteviking\\Desktop\\NCAA-Basketball-Games-Predictor\\kenpom2021.html", "2021")

    
