import argparse
import csv
import json
import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm
from zoomeye import sdk


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog = "find-mobotix",
        description="mobotix camera finder using ZoomEye",
    )
    parser.add_argument("out", help="output directory")
    parser.add_argument("-d", "--dork", default='(/cgi-bin/guestimage.html) -title:"Error 401"')
    parser.add_argument("-p", "--pages", type=int, default=100)
    parser.add_argument("-t", "--connect-timeout", type=float, default=3.05)
    args = parser.parse_args()

    out_path = Path(args.out).resolve()
    if not out_path.exists():
        out_path.mkdir()
    elif not out_path.is_dir:
        raise FileExistsError("Output path cannot be a file")
    
    data_path = out_path / "data.json"
    sites = []
    if data_path.exists():
        with data_path.open() as f:
            sites = json.load(f)
    else:
        print(f"{data_path.as_posix()} not found, requesting {args.pages} pages from ZoomEye...")
        ze = sdk.ZoomEye()
        ze.username = os.environ.get("ZOOMEYE_USERNAME")
        ze.password = os.environ.get("ZOOMEYE_PASSWORD")
        ze.api_key = os.environ.get("ZOOMEYE_API_KEY")
        if ze.username and ze.password:
            ze.login()
        ze.multi_page_search(args.dork, args.pages)
        with data_path.open("w") as f:
            json.dump(ze.data_list, f)
        sites = ze.data_list
    
    cams = []
    timed_out = []
    timeout = args.t, 60
    t = tqdm(sites)
    for site in t:
        service = site["portinfo"]["service"]
        if service not in ("http", "https"):
            service = "http"
        url = "{}://{}:{}/cgi-bin/guestimage.html".format(
            service, site["ip"], site["portinfo"]["port"]
        )
        try:
            r = requests.get(url, verify=False, timeout=timeout)
        except requests.Timeout:
            timed_out.append(url)
            t.write(f"timed out: {url}")
            continue
        except requests.RequestException as e:
            t.write(str(e))
            continue
        if not r.ok:
            t.write(f"error {r.status_code}: {r.url}")
            continue
        cam = {"url": r.url, "timestamp": site["timestamp"]}
        soup = BeautifulSoup(r.text, "html5lib")
        form = soup.find("form", {"name": "dkdk"})
        if form is None:
            t.write(f"skipping {r.url} - no form")
            continue
        options = form.find("select", {"name": "recordmult"}).find_all("option")
        cam["spf"] = max(float(opt.attrs["value"]) for opt in options)
        if title := form.find("title"):
            cam["title"] = title.get_text(strip=True)
        if geo := site.get("geoinfo"):
            if country := geo.get("country") or site.get("continent"):
                cam["country"] = country["names"]["en"]
            if city := geo.get("city"):
                cam["city"] = city["names"]["en"]
        cams.append(cam)
        t.write(f"found cam: {r.url}")
    
    with (out_path / "timed-out.txt").open("w") as f:
        f.writelines(timed_out)
    cams_path = out_path / "cams.csv"
    with cams_path.open("w") as f:
        w = csv.DictWriter(f, ["url", "title", "timestamp", "spf", "country", "city"])
        w.writeheader()
        w.writerows(cams)
    print(f"saved {len(cams)} cams to {cams_path.as_posix()}")


if __name__ == "__main__":
    main()
