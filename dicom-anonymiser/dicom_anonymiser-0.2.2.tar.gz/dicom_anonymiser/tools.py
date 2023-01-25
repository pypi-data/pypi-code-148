"""
Author: Eric Pace
This file is part of dicom_anonymiser.

dicom_anonymiser is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation version 3.

dicom_anonymiser is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Patient CT Contour.
If not, see <https://www.gnu.org/licenses/>.
"""


import os
import pydicom
from pydicom.tag import Tag
from collections import namedtuple
from pathlib import Path
import logging
from datetime import datetime
import csv


Filter = namedtuple('Filter', ['id', 'description', 'value', 'long_desc'])

now = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

root = Path(os.path.abspath(__file__)).parent
logpath = root / 'logs'
ANON_LOG_FILE = logpath / f"{now}.log"


if not os.path.exists(logpath):
    os.makedirs(logpath)

logging.basicConfig(filename=ANON_LOG_FILE,
                    filemode='a',
                    format='%(asctime)s %(levelname)s \t %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def generate_meta_tags():
    tags = []

    f = Path(os.path.abspath(__file__)).parent / 'tags' / 'meta_tags.csv'

    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            tag = Tag([int(x, 16) for x in row[0].split(",")])
            tags.append(tag)

    return tags


def generate_tags(user_list):
    tags = []
    for line in user_list:
        line = Filter(*line)
        tag = Tag([int(x, 16) for x in line.id.split(",")])  # Convert hex to int and get Tag
        tags.append(Filter(tag, line.description, line.value, line.long_desc))
    return tags


def load_dicom_file(filepath):
    try:
        return pydicom.dcmread(os.path.join(filepath))
    except pydicom.errors.InvalidDicomError:
        logging.error(f"Invalid DICOM: {filepath}")
        return None


def save_dicom_file(ds, savepath):
    savepath.parent.mkdir(parents=True, exist_ok=True)
    ds.save_as(str(savepath))
    print(f"Saving: {savepath}\n")
    logging.info(f"Saving: {savepath}\n\n")


def scrub_tags(ds, tags, meta_tag_list):
    for tag in tags:
        try:
            if tag.id in meta_tag_list:
                value_cur = ds.file_meta[tag.id].value
                value_new = tag.value
                ds.file_meta[tag.id].value = value_new

            elif tag.id == Tag([0x0008, 0x1110]) or tag.id == Tag([0x0008, 0x1140]) or tag.id == Tag([0x0008, 0x2112]):
                for seq in ds[tag.id]:
                    seq[0x0008,0x1155].value = '1.2.3.4'
                    seq[0x0008,0x1150].value = '1.2.3.4'

            elif tag.id == Tag([0x0040, 0x0275]):
                del ds[tag.id]

            else:
                value_cur = ds[tag.id].value
                value_new = tag.value
                ds[tag.id].value = value_new

            logging.info(f"{tag.id} {tag.description}: Found (replacing {value_cur} with {value_new})")

        except KeyError:
            logging.info(f"{tag.id} {tag.description}: Tag not present in source file (KeyError)")
        except AttributeError:
            logging.error(f"{tag.id} {tag.description}: Not found (AttributeError)")
        except TypeError:
            logging.error(f"{tag.id} {tag.description}: Not found (TypeError)")
        except:
            logging.error(f"{tag.id} {tag.description}: Unexpected error")

    return ds


def anonymise_file(source_filepath, dest_filepath, tags):
    f = Path(source_filepath)
    ds = load_dicom_file(source_filepath)
    original_accession_number = ds.AccessionNumber

    if ds:
        print(f"Opening: {f}")
        logging.info(f"Opening: {f}")

        meta_tag_list = generate_meta_tags()
        ds_anon = scrub_tags(ds, tags, meta_tag_list)

        # Test for presence of Accession number. Any presence should be logged as a warning
        tag_search(ds, original_accession_number)

        # savefile = os.path.join(f.parent, f"{f.stem}_anon.dcm")
        save_dicom_file(ds_anon, dest_filepath)


def tag_search(ds, substring):
    """
    This is useful to point out any remaining instances of `substring` in the dataset, e.g. accession numbers
    Using iterall() also searches any nested tags
    :param ds: Pydicom dataset
    :param substring: string to search
    :return:
    """
    for de in ds.iterall():
        try:
            if substring in de.value:
                logging.warning(f"{substring} present in anonymised dataset: {de}")
        except TypeError:
            # Not everything is a string.
            pass
