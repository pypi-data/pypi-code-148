import os
import sys
import csv

from pathlib import Path
from typing import Optional, Sequence

from tqdm import tqdm

from c2dn.client import Clip2NetClient
from c2dn.utils import slugify

FIELDS = ('file_id', 'file_name', 'folder_id', 'folder_name', 'short_url', 'long_url', 'local_path')


def main(args: Optional[Sequence[str]] = None) -> None:
    if not args:
        args = sys.argv[1:]

    try:
        username, password, output_dir = args
    except ValueError:
        print('Usage: ./c2dn.py username password output_dir')
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    all_files = {}
    print('Analyzing...')
    with open(Path(output_dir) / 'report.csv', 'wt') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        csv_writer.writeheader()
        with Clip2NetClient(username, password) as client:
            for folder in client.dir():
                files = client.ls(folder)
                print(f'[>] {folder.name} (id:{folder.uid}) [{len(files)} files]:')
                for file in files:
                    print(f'\t{file.name} (id:{file.uid}) -> {file.short_url}, {file.long_url}')
                    file_name = slugify(file.name)
                    local_path = Path(output_dir) / Path(file_name).with_suffix('.' + file.uid + Path(file_name).suffix)
                    csv_writer.writerow({
                        'file_id': file.uid,
                        'file_name': file.name,
                        'folder_id': file.parent.uid,
                        'folder_name': file.parent.name,
                        'short_url': file.short_url,
                        'long_url': file.long_url,
                        'local_path': local_path,
                    })
                    all_files[local_path] = file

    print('\nDownloading...')
    for local_path, file in tqdm(all_files.items()):
        download_url = file.short_url
        if not download_url:
            download_url = file.long_url
        Clip2NetClient.download_file(download_url, local_path)


if __name__ == '__main__':
    main()
