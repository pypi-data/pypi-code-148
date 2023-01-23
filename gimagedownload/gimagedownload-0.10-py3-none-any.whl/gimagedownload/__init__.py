import argparse
import os
import random
import re
import shutil
import sys
import urllib
from time import sleep
from PIL import Image
import requests
from tolerant_isinstance import isinstance_tolerant
from site2hdd import download_url_list, site2hddvars
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
import pandas as pd
from list_all_files_recursively import get_folder_file_complete_path
from get_consecutive_filename import get_free_filename
from url_analyzer import get_all_links_from_html


def main(
    save_fold,
    searchfor,
    ProxyPickleFile,
    howmanyproxiessearch=4,
    threadlimit=150,
    RequestsTimeout=4,
    ThreadTimeout=6,
    try_each_url_n_times=2,
    ProxyConfidenceLimit=0,

):
    checkifgoogle = b'<!doctype html><html lang="en"'
    allpixreg = re.compile(
        "(?:\\.bmp|\\.dib|\\.jpeg|\\.jpg|\\.jpe|\\.jp2|\\.png|\\.webp|\\.pbm|\\.pgm|\\.ppm|\\.sr|\\.ras|\\.tif|\\.tiff|\\.gif|\\.ico)",
        flags=re.IGNORECASE,
    )
    if not os.path.exists(save_fold):
        os.makedirs(save_fold)
    pd_add_apply_ignore_exceptions()

    pornblocker = os.path.normpath(os.path.join(os.getcwd(), "pornblock.txt"))

    html_download = os.path.normpath(os.path.join(save_fold, "htmltemp"))
    if not os.path.exists(html_download):
        os.makedirs(html_download)
    picsavefolder0 = os.path.normpath(os.path.join(save_fold, "pics_html"))
    picsavefolder1 = os.path.normpath(os.path.join(save_fold, "pics_sorted_site"))
    flatresultfolder = os.path.normpath(os.path.join(save_fold, "pics_final"))

    stylew = [
        "".join(
            [
                y.lower() if random.randrange(0, 10) % 2 == 0 else y.upper()
                for y in searchfor
            ]
        )
        for x in range(howmanyproxiessearch)
    ]

    if not os.path.exists(pornblocker):
        res = requests.get(
            "https://raw.githubusercontent.com/Bon-Appetit/porn-domains/master/block.txt"
        )
        with open(pornblocker, mode="wb") as f:
            f.write(res.content)

    with open(pornblocker, mode="r", encoding="utf-8") as f:
        blockdomains = f.read()

    blockdomains = [x.strip() for x in blockdomains.splitlines()]
    urls = [
        rf"https://www.google.com/search?q={urllib.parse.quote(x)}&tbm=isch&hl=en"
        for x in stylew
    ].copy()

    download_url_list(
        urls,
        ProxyPickleFile=ProxyPickleFile,
        # The file you created using the function: get_proxies
        SaveFolder=html_download,  # where should the files be saved
        try_each_url_n_times=try_each_url_n_times,  # maximum retries for each url
        ProxyConfidenceLimit=ProxyConfidenceLimit,
        # each link will be downloaded twice and then compared. If only one result is positive, it counts as a not successful download. But if     the ProxyConfidenceLimit is higher, then it will be accepted
        ThreadLimit=threadlimit,  # downloads at the same time
        RequestsTimeout=RequestsTimeout,  # Timeout for requests
        ThreadTimeout=ThreadTimeout,  # Should be a little higher than RequestsTimeout
        SleepAfterKillThread=0.1,  # Don't put 0.0 here - it will use too much CPU
        SleepAfterStartThread=0.1,  # Don't put 0.0 here - it will use too much CPU
        IgnoreExceptions=True,
        save_as_tmp_dataframe=True,
    )

    df = pd.concat(site2hddvars.all_dataframes).copy()
    df = df.dropna(subset="aa_response").reset_index(drop=True)
    df = (
        df.loc[
            df.aa_response.ds_apply_ignore(
                False,
                lambda x: True if x.content[:30] == checkifgoogle else False,
            )
        ]
        .reset_index(drop=True)
        .copy()
    )

    htmlcode = (
        df.aa_response.ds_apply_ignore(pd.NA, lambda x: x.content)
        .dropna()
        .reset_index(drop=True)
    )
    dfa = htmlcode.ds_apply_ignore(
        pd.NA, lambda x: get_all_links_from_html("https://google.com", x)
    ).dropna()
    dfa2 = pd.concat(dfa.to_list(), ignore_index=True)
    dfa3 = dfa2.drop_duplicates().copy()
    dfli = dfa3.loc[
        (dfa3.aa_is_relative == False) & (~dfa3.aa_domain.isin(["gstatic", "google"]))
    ]
    dfli = dfli.loc[~dfli.aa_domain_w_tl.isin(blockdomains)].reset_index(drop=True)
    urls = dfli.aa_url_query.to_list().copy()
    site2hddvars.all_dataframes = []
    download_url_list(
        urls,
        ProxyPickleFile=ProxyPickleFile,
        # The file you created using the function: get_proxies
        SaveFolder=picsavefolder0,  # where should the files be saved
        try_each_url_n_times=try_each_url_n_times,  # maximum retries for each url
        ProxyConfidenceLimit=ProxyConfidenceLimit,
        # each link will be downloaded twice and then compared. If only one result is positive, it counts as a not successful download. But if     the ProxyConfidenceLimit is higher, then it will be accepted
        ThreadLimit=threadlimit,  # downloads at the same time
        RequestsTimeout=RequestsTimeout,  # Timeout for requests
        ThreadTimeout=ThreadTimeout,  # Should be a little higher than RequestsTimeout
        SleepAfterKillThread=0.1,  # Don't put 0.0 here - it will use too much CPU
        SleepAfterStartThread=0.1,  # Don't put 0.0 here - it will use too much CPU
        IgnoreExceptions=True,
        save_as_tmp_dataframe=True,
    )

    dfg = pd.concat(site2hddvars.all_dataframes, ignore_index=True).dropna(
        subset="aa_response"
    )
    dfg = dfg.loc[
        dfg.aa_response.astype("string").str.contains("[200]", regex=False, na=False)
    ].reset_index(drop=True)
    asu = dfg.ds_apply_ignore(
        pd.NA,
        lambda x: get_all_links_from_html(
            x["aa_downloadlink"], x["aa_response"].content
        ),
        axis=1,
    )
    dfnax = pd.concat(asu.to_list(), ignore_index=True).copy()

    site2hddvars.all_dataframes = []
    dfbi = dfnax.loc[dfnax.aa_filetype.str.contains(allpixreg, na=False)]
    u = dfbi["aa_url_noquery"].to_list()
    download_url_list(
        u,
        ProxyPickleFile=ProxyPickleFile,
        # The file you created using the function: get_proxies
        SaveFolder=picsavefolder1,  # where should the files be saved
        try_each_url_n_times=try_each_url_n_times,  # maximum retries for each url
        ProxyConfidenceLimit=ProxyConfidenceLimit,
        # each link will be downloaded twice and then compared. If only one result is positive, it counts as a not successful download. But if     the ProxyConfidenceLimit is higher, then it will be accepted
        ThreadLimit=threadlimit,  # downloads at the same time
        RequestsTimeout=RequestsTimeout,  # Timeout for requests
        ThreadTimeout=ThreadTimeout,  # Should be a little higher than RequestsTimeout
        SleepAfterKillThread=0.1,  # Don't put 0.0 here - it will use too much CPU
        SleepAfterStartThread=0.1,  # Don't put 0.0 here - it will use too much CPU
        IgnoreExceptions=True,
    )

    fi = get_folder_file_complete_path(folders=[picsavefolder1])
    for file in fi:

        try:
            Image.open(file.path)
            fname = get_free_filename(
                folder=flatresultfolder, fileextension=file.ext, leadingzeros=5
            )
            shutil.copy(file.path, fname)
        except Exception as fe:
            continue

    site2hddvars.all_dataframes = []


def start_image_download(
    ProxyPickleFile,
    search_terms,
    download_folder,
    search_variations=3,
    threadlimit=50,
    RequestsTimeout=7,
    ThreadTimeout=9,
):

    if not isinstance_tolerant(search_terms, list):
        search_terms = [search_terms]
    search_stuff = search_terms.copy()
    mainfolder = download_folder
    for s in search_stuff:
        sav = os.path.normpath(os.path.join(mainfolder, s.replace(" ", "_")))
        try:
            main(
                save_fold=sav,
                searchfor=s,
                howmanyproxiessearch=search_variations,
                threadlimit=threadlimit,
                RequestsTimeout=RequestsTimeout,
                ThreadTimeout=ThreadTimeout,
                ProxyPickleFile=ProxyPickleFile,
            )
        except Exception as fe:
            print(fe)
        sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="GOOGLE IMAGE DOWNLOADER")
        parser.add_argument(
            "-p",
            "--proxy_pickle_file",
            type=str,
            help=f"PKL -> pip install freeproxydownloader",
        )

        parser.add_argument(
            "-s",
            "--search",
            type=str,
            help=f"Comma-separated search terms",
        )

        parser.add_argument(
            "-d",
            "--download_folder",
            type=str,
            help=f"Download path",
            default=os.path.join(os.getcwd(), "GOOGLE_IMAGE_DOWNLOADS"),
        )

        parser.add_argument(
            "-v",
            "--variations",
            type=int,
            help=f"Grab links from slightly different search terms\ndog/DoG/Dog/doG\nwith different proxies. Don't exaggerate. It might get very slow",
            default=3,
        )

        parser.add_argument(
            "-t",
            "--threads",
            type=int,
            help=f"How many threads",
            default=50,
        )

        parser.add_argument(
            "-r",
            "--requests_timeout",
            type=int,
            help=f"Timeout in seconds for requests",
            default=7,
        )

        parser.add_argument(
            "-q",
            "--thread_timeout",
            type=int,
            help=f"Timeout in seconds for running thread. Should be higher than the timeout for requests",
            default=9,
        )
        args = parser.parse_args()
        print(args)

        proxy_pickle_file = args.proxy_pickle_file
        search_terms = [
            x.strip().replace('_', ' ' ) for x in str(args.search).split(",") if x.strip() != ""
        ]
        download_folder = args.download_folder
        search_variations = args.variations
        threadlimit = args.threads
        requests_timeout = args.requests_timeout
        thread_timeout = args.thread_timeout

        start_image_download(
            ProxyPickleFile=proxy_pickle_file,
            search_terms=search_terms,
            download_folder=download_folder,
            search_variations=search_variations,
            threadlimit=threadlimit,
            RequestsTimeout=requests_timeout,
            ThreadTimeout=thread_timeout,
        )



