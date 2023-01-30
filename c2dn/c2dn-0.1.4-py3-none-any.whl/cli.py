import os
import sys
import csv

from pathlib import Path
from typing import Optional, Sequence, Dict

from tqdm import tqdm

from c2dn.client import Clip2NetClient, Clip2NetFile
from c2dn.utils import slugify, url_to_fname, is_c2n_url, get_file_ext

FIELDS = ('file_id', 'file_name', 'timestamp', 'folder_id', 'folder_name', 'short_url', 'long_url', 'local_path')


def main(args: Optional[Sequence[str]] = None) -> None:
    if not args:
        args = sys.argv[1:]

    try:
        username, password, output_dir = args
    except ValueError:
        print('Usage: ./c2dn.py username password output_dir')
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    all_files: Dict[Path, Clip2NetFile] = {}

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
                    # TODO: Refactor this stuff, such an awful impl
                    if not file_name:
                        file_name = url_to_fname(file.long_url) if is_c2n_url(file.long_url) else url_to_fname(file.short_url)
                    local_path = Path(output_dir) / Path(file_name).with_suffix('.' + file.uid + Path(file_name).suffix)
                    if local_path.suffix == f'.{file.uid}':
                        local_path = Path(str(local_path) + get_file_ext(file))
                    csv_writer.writerow({
                        'file_id': file.uid,
                        'file_name': file.name,
                        'timestamp': file.timestamp,
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
        # TODO: Make an optional overwrite
        if not local_path.exists():
            broken_path = local_path.with_suffix('')
            if broken_path.suffix == f'.{file.uid}' and broken_path.exists():
                new_local_path = Path(str(broken_path) + get_file_ext(file))
                print(f'[*] Renaming {broken_path} to {new_local_path}')
                broken_path.rename(new_local_path)
            else:
                Clip2NetClient.download_file(download_url, local_path)
        else:
            print(f'[-] Skipping {download_url}, file exists in the output directory')


if __name__ == '__main__':
    main()
