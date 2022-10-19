#
# https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python
#
# Adapted to scrape NCAA D1 Basketball Data from https://www.sports-reference.com/cbb/seasons/2022-school-stats.html

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, urljoin

def get_soup(url):
    session = requests.Session()
    html = session.get(url)
    return bs(html.content, "html.parser")

def get_all_tables(soup):
    return soup.find_all("table")

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
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")

def get_school_url(row):
    school_url = []
    for a_tag in row.find_all("a"):
        school_url.append(a_tag.text.strip())
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin("https://www.sports-reference.com/cbb/seasons/2022-school-stats.html", href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        gamelog = href.replace(".html", "-gamelogs.html")
        school_url.append(gamelog)
        print ("href --> ",school_url," ",gamelog)
    return school_url

def get_table_rows_url(table):
    """Given a table, returns all its rows along with URL in table"""
    rows = []
    game_logs = []
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
            # use regular th and td tags
            tds = tr.find_all(["td","th"])
            for td in tds:
                cells.append(td.text.strip())
            rows.append(cells)
            #
            # Get School Game Logs url
            #
            game_logs.append(get_school_url (tr))
    #
    # Return Rows of the School Stats Table alomg with Rows of the School an URL
    #
    return rows, game_logs

def get_game_table_rows(school, table):
    """Given a school and a Game Logs table, returns all its rows in table"""
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
            # use regular th and td tags
            tds = tr.find_all(["td","th"])
            cells.append (school)
            for td in tds:
                cells.append(td.text.strip())
            rows.append(cells)
    return rows

def get_game_logs (game_log):
    school       = game_log[0]
    game_log_url = game_log[1]

    # get the gamesoup
    gamesoup = get_soup(game_log_url)
    # extract all the tables from the web page
    tables = get_all_tables(gamesoup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        school_headers = headers.insert (0, 'School')

        # get all the rows of the table
        rows = get_game_table_rows(school, table)


    return headers, rows

def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    rows = table.find_all("tr")
    for th in rows[1].find_all("th"):
        headers.append(th.text.strip())

    return headers

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

        # get all the rows of the table
        rows, game_logs = get_table_rows_url(table)

        # save table as csv file
        table_name = 'NCAA_school_stats'
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name, headers, rows)

    gl_rows = []
    for game_log in game_logs:
         # get game log data for each school
         print ('Getting Data for --> ', game_log)
         gl_header, gl_school_rows = get_game_logs (game_log)

         for gl_row in gl_school_rows:
             gl_rows.append (gl_row)

    gl_table_name = 'NCAA_Game_Log'
    print(f"[+] Saving {table_name}")
    save_as_csv(gl_table_name, gl_header, gl_rows)

if __name__ == "__main__":
    import sys
    try:
        url = "https://www.sports-reference.com/cbb/seasons/2022-school-stats.html"
        if "sports-reference" not in url:
            print("Invalid URL passed, scraper may not work on this website")
            exit(0)
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(0)
    main(url)

