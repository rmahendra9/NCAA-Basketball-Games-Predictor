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
    df.set_index("Team")
    df.to_csv(f"{table_name}.csv")

def main(url, year):
    # get the soup
    soup = bs(open(url).read(), 'html.parser')
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    final_df = pd.DataFrame()
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers - need to change for each year
        # get all the rows of the table
        if i == 1:    
            headers = ['Team','O-Eff', 'D-Eff', 'SOS', 'R+T']
        elif i == 2:
            headers = ['Team','Seniors8', 'Juniors8', '1/3 Clutch?', '3Pt%', 'F/C 12+ PPG', '2 F/C 20/12']
        elif i == 3:
            headers = ['Team','TS Marg', 'Dbl Fig#', 'OReb%', '2Pt%D', 'FTR', 'DFT Rat']
        elif i == 4:
            headers = ['Team', 'Champions', 'Coach Exp.', 'Scoring Margin', 'FG% Diff', 'Win Strk']
        rows = get_table_rows(table)
        df = pd.DataFrame(rows, columns=headers)
        if i == 1:
            final_df = pd.concat([final_df, df])
        else:
            final_df = pd.merge(final_df, df, on='Team', how='inner')
    rows = final_df.values
    headers = final_df.columns
    ss_table_name = 'Additional_Stats_' + year
    print(f"[+] Saving {ss_table_name}")
    save_as_csv(ss_table_name, headers, rows)
    


if __name__ == "__main__":
    main(r"C:\\Users\\theeliteviking\\Desktop\\NCAA-Basketball-Games-Predictor\\additional_stats_2021.html", "2021")

    
