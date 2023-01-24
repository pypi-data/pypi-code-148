"""This module will contain functions to handle image processing functions"""

from datetime import datetime
import logging
import re
import cv2
import fitz
import numpy as np

logger = logging.getLogger(__name__)

def process_pdf(path:str=None, bytes_io: bytes = None, image_max: int = 5, dpi: int=300):
    """Will open the PSF file and rerurn a set of images and metadata"""
    # Date string: D:20180611144927-04'00'
    #                Y4  M2D2H2m2S2-Z2'ZM2'
    dtreg = re.compile(r"D:(?P<year>[\d]{4})(?P<month>[\d]{2})(?P<day>[\d]{2})(?P<hour>[\d]{2})(?P<min>[\d]{2})(?P<sec>[\d]{2})(?P<zulu>[\-]{0,1}[\d]{2}'[\d]{2}')")
    if path is not None:
        fobj = fitz.open(path)
    elif bytes_io is not None:
        fobj = fitz.open("pdf", bytes_io)
    else:
        # need something to open
        raise Exception(msg="Need a file path or byte object to open")

    data = {
        "metadata": fobj.metadata,
        "toc": fobj.get_toc(),
        "texts": [],
        "images": [],
        "pages": [],
        "count": 0
    }

    for fld in ["creationDate", "modDate"]:
        if dtstr := data.get("metadata",{}).get(fld):
            if m := dtreg.match(dtstr):
                dt = {}
                for rfld in ["year", "month", "day", "hour", "min", "sec", "zulu"]:
                    dt[rfld] = m.group(rfld)
                data["metadata"][fld] = \
                    f"{dt['year']}-{dt['month']}-{dt['day']} {dt['hour']}:{dt['min']}:{dt['sec']} Z{dt['zulu']}"

    for i, pg in enumerate(fobj, start=1):
        # get the page
        logger.debug("Page: W: %s H: %s MNW: %s MBH: %s",
                pg.rect.width, pg.rect.height, pg.mediabox.width, pg.mediabox.height)
        data["pages"].append({
            "width": pg.rect.width,
            "height": pg.rect.height,
            "mediabox": {
                "width": pg.mediabox.width,
                "height": pg.mediabox.height
            }
        })

        if textblock := pg.get_text("blocks"):
            data["texts"].append(textblock)

        for link in pg.links():
            if "links" not in data:
                data["links"] = []
            data["links"].append(link)

        for annot in pg.annots():
            if "notes" not in data:
                data["notes"] = []
            data["notes"].append(annot)

        for widget in pg.widgets():
            if "widgets" not in data:
                data["widgets"] = []
            data["widgets"].append(widget)

        if imgs := pg.get_images():
            if "figures" not in data:
                data["figures"] = []

            for img in imgs:
                data["figures"].append(img)

        # dump a pixmap
        if i <= image_max:
            pix = pg.get_pixmap(dpi=dpi) #(matrix = mat)
            img_data = pix.pil_tobytes(format="PNG", optimize=True)
            nparr = np.frombuffer(img_data, np.uint8)
            data["images"].append(cv2.imdecode(nparr, cv2.IMREAD_COLOR))

    data["count"] = i
    fobj = None

    return data

def make_pdf_images(path:str=None, bytes_io: bytes = None, first_page: bool = True, dpi: int=300) -> list:
    """Will return the pages as images"""
    images = []
    if path is not None:
        fobj = fitz.open(path)
    elif bytes_io is not None:
        fobj = fitz.open("pdf", bytes_io)
    else:
        # need something to open
        raise Exception(msg="Need a file path or byte object to open")

    for i, pg in enumerate(fobj, start=1):
        pix = pg.get_pixmap(dpi=dpi)
        img_data = pix.pil_tobytes(format="PNG", optimize=True)
        nparr = np.frombuffer(img_data, np.uint8)
        img_data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        logger.info("[%s] ORIG: %s", i, img_data.shape)
        images.append(img_data)
        if first_page is True:
            break

    return images

def make_pdf_thumbnail(path:str=None, bytes_io: bytes = None, first_page: bool = True, size: int=300) -> list:
    """Will open the pdf file specified and create a thumbnail for the first
    image_max pages:"""
    images = []
    if path is not None:
        fobj = fitz.open(path)
    elif bytes_io is not None:
        fobj = fitz.open("pdf", bytes_io)
    else:
        # need something to open
        raise Exception(msg="Need a file path or byte object to open")

    for i, pg in enumerate(fobj, start=1):
        pix = pg.get_pixmap()
        img_data = pix.pil_tobytes(format="PNG", optimize=True)
        nparr = np.frombuffer(img_data, np.uint8)
        img_data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        logger.info("[%s] ORIG: %s", i, img_data.shape)
        img_data = cv2.resize(img_data, dsize=(size, size), interpolation=cv2.INTER_AREA)
        logger.info("[%s] Resize: %s", i, img_data.shape)
        images.append(img_data)
        if first_page is True:
            break

    return images
