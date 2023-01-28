import logging
import os
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Optional

import requests
import typer
import xlsxwriter
from selenium import webdriver

from dumbo_scopus.utils import is_file_open_by_other_processes

SEARCH_ENDPOINT = "https://api.elsevier.com/content/search/scopus"

SCOPUS_ID_PATTERN = re.compile(r"2-s2\.0-[0-9]+")

DEFAULT_OUTPUT_FILENAME = "scopus"
MAX_NUMBER_OF_RESULTS_PER_REQUEST = 25


app = typer.Typer()


@app.command("search")
def scopus_search(
        query: str = typer.Argument(..., help="A query as described in https://dev.elsevier.com/sc_search_tips.html\n"
                                              "For example, 'TITLE(magic sets)'"),
        api_key: str = typer.Option(..., "--api-key", "-k", envvar="SCOPUS_API_KEY",
                                    help="Your Scopus API key from https://dev.elsevier.com/"),
        number_of_results: int = typer.Option(MAX_NUMBER_OF_RESULTS_PER_REQUEST, "--number-of-results", "-n",
                                              help="The number of wanted results"),
        output_filename: Path = typer.Option(f"{DEFAULT_OUTPUT_FILENAME}.xlsx", "--output-filename", "-o",
                                             help="The path to the output file to be produced (must be writable)"),
        with_log: bool = typer.Option(False, "--with-log", "-l", help="Print logging information"),
) -> None:
    if with_log:
        logging.getLogger().setLevel(logging.INFO)
    logging.info(f"Starting SCOPUS search for query {query} (up to {number_of_results} results)")
    keys = set()
    entries = []
    while len(entries) < number_of_results:
        logging.info(f"Results so far: {len(entries)}")

        res = requests.get(SEARCH_ENDPOINT, params={
            "query": query,
            "apiKey": api_key,
            "start": len(entries),
            "count": MAX_NUMBER_OF_RESULTS_PER_REQUEST,
        })
        if res.status_code != 200:
            print(f"Unexpected status code: {res.status_code}")
            break

        data = res.json()
        data = data['search-results']
        if 'entry' not in data:
            logging.info(f"No results in the last query. All results already retrieved.")
            break
        data = data['entry']

        for index, entry in enumerate(data):
            keys.update(entry.keys())
            entries.append(entry)
        logging.info(f"Added {len(data)} results")

        if len(data) < MAX_NUMBER_OF_RESULTS_PER_REQUEST:
            logging.info(f"There was space for more results, but have not been found. All results already retrieved.")
            break

    keys = list(sorted(keys))
    logging.info(f"Writing {len(entries)} results to {output_filename}")
    rows = [[str(key) for key in keys]]
    for entry in entries:
        rows.append([str(entry[key]) if key in entry.keys() else None for key in keys])

    with xlsxwriter.Workbook(output_filename) as workbook:
        worksheet = workbook.add_worksheet()
        for index, row in enumerate(rows):
            worksheet.write_row(index, 0, row)


@app.command("citations")
def scopus_citations(
        scopus_id: str = typer.Argument(..., help="The Scopus ID of the queried article. "
                                                  "For example, 2-s2.0-84949895809"),
        proxy: Optional[str] = typer.Option(None, help="Proxy server for the Chrome browser"),
        output_filename: Path = typer.Option(f"{DEFAULT_OUTPUT_FILENAME}.csv", "--output-filename", "-o",
                                             help="The path to the output file to be produced (must be writable)"),
        show_browser: bool = typer.Option(False, "--show-browser", "-s", help="Show all automatic interactions with "
                                                                              "the browser"),
        with_log: bool = typer.Option(False, "--with-log", "-l", help="Print logging information"),
) -> None:
    if with_log:
        logging.getLogger().setLevel(logging.INFO)

    with tempfile.TemporaryDirectory() as temporary_directory:
        logging.info("Setting up Chrome...")
        options = webdriver.ChromeOptions()
        options.headless = not show_browser
        options.add_experimental_option("detach", show_browser)
        if not show_browser:
            options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/60.0.3112.50 Safari/537.36')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        options.add_experimental_option('prefs', {'download.default_directory': temporary_directory})
        driver = webdriver.Chrome(options=options)

        logging.info("Visiting citations web page (may take a few seconds)...")
        driver.get(f'https://www.scopus.com/results/citedbyresults.uri?sort=plf-f&src=s&sot=cite&cite={scopus_id}')
        logging.info("Selecting all documents...")
        driver.execute_script("document.getElementById('mainResults-selectAllTop').click()")
        logging.info("Asking to export...")
        driver.execute_script("document.getElementById('export_results').click()")
        logging.info("as CSV...")
        driver.execute_script("document.getElementById('CSV').click()")
        logging.info("and confirm...")
        driver.execute_script("document.getElementById('exportTrigger').click()")
        logging.info("Download command issued...")

        while True:
            for filename in os.listdir(temporary_directory):
                path = Path(temporary_directory) / filename
                if not is_file_open_by_other_processes(path):
                    shutil.copy(path, output_filename)
                    logging.info("Download complete!")
                    driver.close()
                    return

            logging.info("Still downloading...")
            time.sleep(1)
