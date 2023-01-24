"""This module will contain functions to handle image processing functions"""

from datetime import datetime
import logging
import cv2
import math
import numpy as np
import pytesseract
import statistics

from collections import namedtuple
from lost_cat_images.utils.utils_shapes import Rectangle, intersect, merge, ShapeGrouper, printTree

logger = logging.getLogger(__name__)

Contour = namedtuple("Contour", ["x", "y", "w", "h", "p", "c", "a"])

def extactImageContours(img: np.array, markup:np.ndarray=None, config: dict = None,
        minheight: int = 30, minwidth: int = 30,
        grid: int = -1, bleed: int = 4,
        max_r: int = 120, fidx: int = None, save_steps: bool = False
    ) -> dict:
    """
    """
    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = img.copy()

    if config is None:
        config = {
            "mode": cv2.RETR_TREE,
            "method": cv2.CHAIN_APPROX_SIMPLE
        }

    logger.debug("EIC: {%s} H:%s W:%s G:%s", fidx, minheight, minwidth, grid)

    # check the grid
    if grid == -1:
        iw = img.shape[1]
        grid = minwidth // 2

    # process the image...
    contours, _ = cv2.findContours(image=img, **config)
    cv2.drawContours(image=img_return, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1)

    # now to extract rectangles from the image...
    font = cv2.FONT_HERSHEY_SIMPLEX
    found = []
    idx = -1
    cidx = 0
    bidx = 0
    yc = 6629
    xc = 8074 # 6629, 6753, 8074, 8154
    borders = []

    for c in contours: #.sort(key=lambda r: [int(minheight * round(float(r[1]) / minheight)), int(minwidth * round(float(r[0]) / minwidth))]):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # look for any contours that contain the selected pixel
        (bbx,bby,bbw,bbh) = cv2.boundingRect(c)
        (ibx,iby,ibw,ibh) = cv2.boundingRect(c)

        if minwidth >= bbw or minheight >= bbh:
            continue

        # detect border % black to white pixels...
        bbxt, bbyt, bbxb, bbyb = bbx-bleed, bby-bleed, bbx+bbw+bleed, bby+bbh+bleed

        crop = img[bby:bby+bbh, bbx:bbx+bbw]
        pixels1 = img[bbyt:bbyb, bbxt:bbxt+bleed]
        pixels2 = img[bbyt:bbyb, bbxb-bleed:bbxb]
        pixels3 = img[bbyt:bbyt+bleed, bbxt:bbxb]
        pixels4 = img[bbyb-bleed:bbyb, bbxt:bbxb]
        pixsum = (pixels1.sum() + pixels2.sum() + pixels3.sum() + pixels4.sum())
        pixsize = (pixels1.size + pixels2.size + pixels3.size + pixels4.size)

        border_ratio =  pixsum / pixsize if pixsize > 0 else 0

        contents_ratio = crop.sum() / crop.size if crop.size > 0 else 0

        idx += 1
        #if save_steps:
        #    cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.IC.png', crop)

        logger.debug("Crop: %s", idx)
        logger.debug("Counts: C: %s => P1: %s P2: %s P3: %s P4: %s", crop.size, pixels1.size, pixels2.size, pixels3.size, pixels4.size)
        logger.debug("Sums:   C: %s => P1: %s P2: %s P3: %s P4: %s", crop.sum(), pixels1.sum(), pixels2.sum(), pixels3.sum(), pixels4.sum())
        logger.debug("Ratios:\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s", fidx, idx, border_ratio / contents_ratio, border_ratio, contents_ratio, bbx, bby, bbw, bbh)

        if border_ratio < max_r:
            cv2.rectangle(img_return, (bbx, bby), (bbx + bbw, bby + bbh), (0, 0, 255), 1)
            cv2.putText(img=img_return, text=str(bidx),
                org=(bbx+10, bby+10), fontFace=font, fontScale=0.5, color=(0, 255, 0),
                thickness=1)

            borders.append(c)
            # use bleed
            found.append((bbxt, bbyt, bbw+(2*bleed), bbh+(2*bleed)))
            # no bleed
            #found.append((bbxt, bbyt, bbw, bbh))
            logger.debug("Box: %s [%s] %s => %s", idx, bidx, (bby,bby+bbh,bbx,bbx+bbw), (bbxt, bbyt, bbw+(2*bleed), bbh+(2*bleed)))
            bidx += 1

    # now print these boxes if they are close to the borders in a table
    boxes = []
    vertices = set()
    logger.debug("Found: %s", len(found))

    for (x,y,w,h) in found:
        xtl, ytl = (x // grid) * grid, (y // grid) * grid
        xtr, ytr = ((x + w) // grid) * grid, (y // grid) * grid
        xbl, ybl = (x // grid) * grid, ((y + h) // grid) * grid
        xbr, ybr = ((x + w) // grid) * grid, ((y + h) // grid) * grid
        logger.debug("Grid: [%s %s %s %s] => [%s %s %s %s]", x, y, w, h, xtl, ytl, xbr, ybr)
        vertices.add((xtl, ytl))
        vertices.add((xtr, ytr))
        vertices.add((xbl, ybl))
        vertices.add((xbr, ybr))

        boxes.append((x,y,w,h))
        cv2.rectangle(img_return, (x, y), (x + w, y + h), (255, 255, 0), 1)
        #cv2.putText(img=img_return, text=('width = {}, height = {}'.format(w, h)),
        #    org=(x+30, y+30), fontFace=font, fontScale=0.5, color=(255, 255, 0),
        #    thickness=1)

    # Hallsm!n!sCannonsAddr3ss
    logger.debug("Vertices: %s", len(vertices))
    for (x,y) in vertices:
        cv2.circle(img=img_return, center=(x, y), radius=(grid // 2), color=(255,0,255), thickness=1)
        cv2.circle(img=img_return, center=(x, y), radius=(grid), color=(255,0,255), thickness=2)

    return {
        "image": img_return,
        "borders": borders,
        "boxes": boxes
    }

def box_connected(img:np.ndarray, markup:np.ndarray=None,
        boxes:list= None, contours:list = None,
        fidx:int = None, bleed:int = 3, save_steps:bool = False) -> list:
    """Will take the gioven boxes and selected the boxes of interest."""
    dims = img.shape
    ix,iy = dims[0], dims[1]
    par_chld_w = []

    logger.debug("BC: {%s:--} B:%s C:%s", fidx, len(boxes), len(contours))

    conn_box = [None] * len(boxes)
    Box = namedtuple("Box", "idx x y w h")

    trbox = Box(-1, 0, 0, 0, iy)
    brbox = Box(-1, 0, 0, 0, 0)

    # echeck for for heirachy and connected edges
    for idx, (tx,ty,bw,bh) in enumerate(boxes):
        bx = tx + bw
        by = ty + bh
        logger.debug("Box: %s => %s", idx, (tx,ty,bw,bh))
        label = f"{tx}:{ty}:{bw}:{bh}"

        if ((trbox.x + trbox.w) < (tx + bw) or
                (trbox.y) > (ty)):
            trbox = Box(idx, tx,ty,bw,bh)

        if ((brbox.x + brbox.w) < (tx + bw) or
                (brbox.y) < (ty)):
            brbox = Box(idx, tx,ty,bw,bh)

        # find the connecting boxes...
        for jdx, (ctx,cty,cbw,cbh) in enumerate(boxes):
            if idx == jdx:
                continue

            cbx = ctx + cbw
            cby = cty + cbh

            score = [
                (ctx <= tx <= cbx), (ctx <= bx <= cbx),                                         #  0, 1
                (cty <= ty <= cby), (cty <= by <= cby),                                         #  2, 3
                ((ctx - bleed) <= tx <= (ctx + bleed)), ((ctx - bleed) <= bx <= (ctx + bleed)), #  4, 5 left edge
                ((cty - bleed) <= ty <= (cty + bleed)), ((cty - bleed) <= by <= (cty + bleed)), #  6, 7 top edge
                ((cbx - bleed) <= tx <= (cbx + bleed)), ((cbx - bleed) <= bx <= (cbx + bleed)), #  8, 9 right edge
                ((cby - bleed) <= ty <= (cby + bleed)), ((cby - bleed) <= by <= (cby + bleed)), # 10,11 bottom edge
             ]

            # left or right is connected and y in range or top or bottom is connected and x in range
            if (    ((score[4] is True) or (score[5] is True)) and ((score[2] is True) or (score[3] is True)) or # if left edge and in top bottom
                    ((score[6] is True) or (score[7] is True)) and ((score[0] is True) or (score[1] is True)) or
                    ((score[8] is True) or (score[9] is True)) and ((score[2] is True) or (score[3] is True)) or
                    ((score[10] is True) or (score[11] is True)) and ((score[0] is True) or (score[1] is True))
                ):
                # connected edge
                if conn_box[idx] is None:
                    conn_box[idx] = set()
                conn_box[idx].add(jdx)
                if conn_box[jdx] is None:
                    conn_box[jdx] = set()
                conn_box[jdx].add(idx)

                logger.debug("\t%s <=> %s: %s", idx, jdx, score)

    if logger.level == logging.DEBUG:
        logger.info("Connected:")
        for idx, v in enumerate(conn_box):
            logger.info("\t%s\t%s", idx, v)

        logger.info("\tTR: %s", trbox)
        logger.info("\tBR: %s", brbox)

    # start from BR Box
    selidx = set()
    selidx.add(trbox.idx)
    selidx.add(brbox.idx)
    q = list(selidx)
    while q and len(q) > 0:
        cidx = q.pop()
        # get the connected ids
        if ids := conn_box[cidx]:
            for idx in ids:
                if idx not in selidx:
                    selidx.add(idx)
                    q.append(idx)

    logger.debug("\tCB: %s", selidx)

    # return on the leaf boxes
    selected = []
    borders = []
    logger.info("Selected:")
    for idx in selidx:
        if idx == -1:
            continue

        logger.info("\t%s: %s", idx, boxes[idx])
        selected.append(boxes[idx])
        borders.append(contours[idx])

    return {
        "boxes": selected,
        "borders": borders,
    }

def segmentImage(img:np.array, markup:np.ndarray=None,
        linesize: int = 10, closesize: int = 5, linewidth: int = 1,
        factor: int = 3,
        fidx: int=-1, idx: int=-1, save_steps: bool = False) -> dict:
    """will use the v and h line processes and then create blocks for potential text
    it'll apply state to the resultant contours
        block ratio
        block height
        block width"""
    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = img.copy()

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    h,w = img.shape[:2]
    img_blank = np.zeros((h,w,3), dtype="uint8")
    img_blank.fill(255)

    # an image for the chosen elements results...
    img_mask = np.zeros(img.shape[:2], dtype="uint8")

    # apply the h and vert transforms
    #horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (linesize,linewidth))
    #detected_lines = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    #vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (linewidth,linesize))
    #detected_lines = cv2.morphologyEx(detected_lines, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
    #if save_steps:
    #    cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.SEG.png', detected_lines)

    # get the contours:
    #sd = ShapeDetector()
    contours, _ = cv2.findContours(image=img.copy(), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    logger.info("SI: {%s:%s} SHP: %s CNTS: %s", fidx, idx, img.shape, len(contours))
    boxes = []
    selected = []
    found = []
    modws = []
    modhs = []

    # quick segementation, too small and to large :)
    for c in contours:
        # update the markup image
        (bbx,bby,bbw,bbh) = cv2.boundingRect(c)
        if (bbw == w) and (bbh == h):
            logger.debug("SI: {%s:%s} C: OUT %s", fidx, idx, (bbx,bby,bbw,bbh))
            continue

        # filter small contours...
        #if (bbh <= closesize) and (bbw <= closesize):
        #    logger.debug("SI: {%s:%s} C: SML %s", fidx, idx, (bbx,bby,bbw,bbh))
        #    continue

        if (bbh > (h * 0.9)) and (bbw > (w + 0.9)):
            logger.debug("SI: {%s:%s} C: LRG %s", fidx, idx, (bbx,bby,bbw,bbh))
            continue

        logger.debug("SI: {%s:%s} C: USE %s", fidx, idx, (bbx,bby,bbw,bbh))
        modhs.append(bbh)
        modws.append(bbw)
        found.append((bbx,bby,bbw,bbh, c))

    logger.debug("SI: {%s:%s} A: F:%s H:%s W:%s", fidx, idx, len(found), len(modhs), len(modws))

    if len(found) == 0:
        return {
            "image": None,
            "boxes": boxes,
            "contours": selected
        }

    # we need to get the modal bounding box h and w...
    maxh = max(modhs)
    maxw = max(modws)
    modh = statistics.mode(modhs)
    modw = statistics.mode(modws)
    logger.info("SI: {%s:%s} MOD: H %s W %s", fidx, idx, modh, modw)

    medh = statistics.median(modhs)
    medw = statistics.median(modws)
    logger.info("SI: {%s:%s} MED: H %s W %s", fidx, idx, medh, medw)
    logger.info("SI: {%s:%s} MAX: H %s W %s", fidx, idx, maxh, maxw)

    # process the found elements
    for cidx, (bbx,bby,bbw,bbh, c) in enumerate(found):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # log and show the results
        logger.debug("SI: {%s:%s:%s} C: %s", fidx, idx, cidx, (bbx,bby,bbw,bbh))
        #logger.debug("SI: {%s:%s:%s} A: %s", fidx, idx, cidx, approx)
        cv2.rectangle(img=img_blank, pt1=(bbx, bby), pt2=(bbx+bbw, bby+bbh), color=(255,0,0), thickness=1)

        cv2.putText(img=img_blank, text=str(cidx),
            org=(bbx, bby), fontFace=font, fontScale=0.5, color=(255, 0, 0),
            thickness=1)

        # check the length of the contour...
        # remove large lines (2 points or less)
        # consider size, number of points in the approx
        if bbh == maxh:
            logger.info("SI: {%s:%s:%s} EXCLUDE %s", fidx, idx, cidx, (bbw, medw, bbh, medh))
            cv2.drawContours(img_blank, [approx], -1, (0,255,0), 1)

        elif (bbw < (medw * factor)) or (bbh < (medh * factor)):
            logger.info("SI: {%s:%s:%s} INCLUDE %s", fidx, idx, cidx, (bbw, medw, bbh, medh))
            cv2.drawContours(img_blank, [approx], -1, (0,0,255), 1)

            # add the conotur to the mask...
            cv2.drawContours(img_mask, [c], -1, (255), -1)
            boxes.append((bbx, bby, bbw, bbh, approx))
            selected.append(approx)
        else:
            logger.info("SI: {%s:%s:%s} EXCLUDE %s", fidx, idx, cidx, (bbw, medw, bbh, medh))
            cv2.drawContours(img_blank, [approx], -1, (0,255,0), 1)

    if save_steps:
        cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.SIC.png', img_blank)

    img_blank = np.zeros(img.shape[:2], dtype="uint8")
    img_blank.fill(255)

    masked = np.where(img_mask, img, img_blank)
    if save_steps:
        cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.BOX.png', masked)

    # return the mask
    return {
        "image": masked,
        "boxes": boxes,
        "contours": selected
    }

def processTableBoxes(img:np.ndarray, markup:np.ndarray=None,
            boxes:list= None, contours:list = None,
            fidx:int = None, use_blur: bool = True,
            bleed: int = 4, mindim: int = 1000,
            config: dict = None,
            save_steps: bool = False) -> dict:
    """will take the supplied images and the boxes, will order the boxes"""
    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = img.copy()

    logger.info("PTB: {%s:--} B:%s C:%s S:%s", fidx, len(boxes), len(contours), img.shape)

    img_edit = img.copy()
    kernelX = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    kernelE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    font = cv2.FONT_HERSHEY_SIMPLEX
    idx = -1
    border = 10

    # a list of the boxes, and found text areas
    rows = []
    for (x,y,w,h) in boxes:
        idx += 1
        # draw the contour as white...
        cv2.drawContours(image=img_edit, contours=contours[idx], contourIdx=-1, color=(255), thickness=bleed)
        #cv2.rectangle(img_edit, (x+bleed, y+bleed), (x + w - (2*bleed), y + h - (2*bleed)), (255), bleed)

        cv2.rectangle(img_return, (x, y), (x + w, y + h), (255, 0, 0), 1)
        cv2.rectangle(img_return, (x+bleed, y+bleed), (x + w - (2*bleed), y + h - (2*bleed)), (255, 255, 0), 1)

        # sele3ct the region to use for anlysis
        crop_img = cv2.copyMakeBorder(src=img_edit[y+bleed:y+h-(2*bleed), x-bleed:x+w-(2*bleed)],
            top=border+bleed,
            bottom=border+bleed,
            left=border+bleed,
            right=border+bleed,
            borderType=cv2.BORDER_CONSTANT,
            value=[255])

        if save_steps:
            cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.O.png', crop_img)

        #crop_img = removeLines(img=crop_img)
        #if save_steps:
        #    cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.REM.png', crop_img)
        # remove speckles and blur
        #crop_img = cv2.dilate(crop_img, kernelE, iterations=1)
        #crop_img = cv2.erode(crop_img, kernelE, iterations=1)
        #if save_steps:
        #    cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.BLU.png', crop_img)

        # get the boxes with potential text info
        text_data = segmentImage(img=crop_img, fidx=fidx, idx=idx, save_steps=save_steps)
        crop_img = text_data.get("image")
        if crop_img is None:
            continue
        if save_steps:
            cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.PTB.png', crop_img)

        if use_blur:
            crop_img = cv2.blur(src=crop_img, ksize=(3,3))
            #crop_img = cv2.erode(crop_img, kernelX, iterations=3)
            #crop_img = cv2.dilate(crop_img, kernelX, iterations=1)

        # create image to put text on...
        ch,cw = crop_img.shape[:2]
        img_text = np.zeros((ch,cw,3), dtype="uint8")
        img_text.fill(255)

        ratio = 1
        if w < mindim or h < mindim:
            mindim = min(w,h)
            ratio = int(config.get("ratio",3))

            rw = int(w * ratio)
            rh = int(h * ratio)
            logger.info("Ratio: {%s:%s} %s %s => %s", fidx, idx, rw, rh, ratio)

            # rescale:
            crop_img = cv2.resize(src=crop_img, dsize=(rw, rh), interpolation = cv2.INTER_AREA)

            # detect text orientation...
            try:
                results = pytesseract.image_to_osd(image=crop_img, output_type=pytesseract.Output.DICT, config='--psm 11 -c min_characters_to_try=5')
                logger.info("OSD: {%s:%s} => %s", fidx, idx, results)
            except Exception as ex:
                logger.error("OSD: {%s:%s} => %s", fidx, idx, ex)

        # hack to fix speckels etc....
        # double size and then shrink
        if ratio == 1:
            crop_img = cv2.resize(src=crop_img, dsize=(w*2, h*2), interpolation = cv2.INTER_AREA)
        else:
            crop_img = cv2.resize(src=crop_img, dsize=(rw*2, rh*2), interpolation = cv2.INTER_AREA)
            crop_img = cv2.erode(crop_img, kernelX, iterations=1)
            crop_img = cv2.dilate(crop_img, kernelX, iterations=1)

        # process the text in the image...
        def_opt = "--psm 12"
        tess_options = config.get("tesseract", {}).get("i2d", def_opt) if config else def_opt
        d = pytesseract.image_to_data(image=crop_img, output_type=pytesseract.Output.DICT, config=tess_options)
        flds = d.keys()
        r = len(d['level'])

        # now shrink the image by 50%
        if ratio == 1:
            crop_img = cv2.resize(src=crop_img, dsize=(w, h), interpolation = cv2.INTER_AREA)
        else:
            crop_img = cv2.resize(src=crop_img, dsize=(rw, rh), interpolation = cv2.INTER_AREA)

        cv2.fillPoly(img=img_return, pts=contours[idx], color=(0,255,255))


        for i in range(r):
            # get the the detected text values...
            if len(d.get("text",[])[i].strip()) == 0:
                continue

            row = {
                "file": fidx,
                "idx": idx
            }
            for f in flds:
                row[f] = d.get(f,[])[i]

            # correct the ratio...
            for f in ['left', 'top', 'width', 'height']:
                row[f] = int(row[f] / ratio)

            # save the crop image for post analysis - debug
            (xt, yt, wt, ht) = (row['left'], row['top'], row['width'], row['height'])
            cv2.putText(img=img_text, text=(row['text']),
                    org=(xt, yt), fontFace=font, fontScale=1, color=(0, 0, 255),
                    thickness=1)

            # apply the offset...
            row['left'] += (x - border)
            row['top'] += (y - border)
            rows.append(row)

            logger.info("Text: {%s:%s} %s", fidx, idx, row)

        # export image...
        if save_steps:
            cv2.imwrite(f'data/eng/crops/F{fidx}.{idx}.TXT.png', img_text)

    return {
        "image": img_return,
        "boxes": rows,
    }

def extract_textareas(image: np.array, config: dict = None) -> dict:
    """The heavy lift function for documents
    will try to extract the following:
        grids: connected boxes
        text: text and it's position
    """
    data = {}
    img = image.copy()
    fidx = config.get("file",{}).get("id", -1)
    logger.info("File IDX: %s", fidx)

    save_steps = config.get("debug", {}).get("save")
    if save_steps:
        logger.debug("Saving Images...")
        data["images"] = {}

    # get some kernels to use...
    kernel_size = config.get("kernel",{}).get("size", 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

    # perform the base processing of the image...
    img_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

    thres_min = config.get("threshold", {}).get("thresh", 75)
    thres_max = config.get("threshold", {}).get("maxval", 255)
    thres_type = config.get("threshold", {}).get("type", cv2.THRESH_BINARY)
    _, img_thresh = cv2.threshold(src=img_gray, thresh=thres_min, maxval=thres_max, type=thres_type)

    # workflow original...
    # extract the contours to see if this can be useful
    contour_data = extactImageContours(img=img_thresh, markup=img,
                config=config.get("contours,{}"), fidx=fidx)

    if save_steps:
        logger.debug("Save Contour Image")
        data["images"]["contours"] = contour_data.get("image")

    if len(contour_data.get("borders",[])) > 0:
        box_data = box_connected(img=img_thresh, markup=img, boxes=contour_data.get("boxes",[]),
                contours=contour_data.get("borders",[]), fidx=fidx, save_steps=save_steps)

        if save_steps:
            logger.debug("Save Box Image")
            data["images"]["boxes"] = box_data.get("image")

        if len(box_data.get("boxes",[])) > 0:
            text_data = processTableBoxes(img=img_thresh, markup=img,
                    boxes=box_data.get("boxes",[]), contours=box_data.get("borders",[]),
                    fidx=fidx, save_steps=save_steps, use_blur=config.get("operations", {}).get("blur", False))

            if save_steps:
                logger.debug("Save Text Image")
                data["images"]["text"] = text_data.get("image")
            data["text"] = text_data.get("boxes", [])

    if save_steps:
        for key,img in data.get("images",{}).items():
            if img is not None and not img.size == 0:
                cv2.imwrite(f'data/eng/F{fidx}.{key}.png', img)

    return data

def process_image(image: np.array, markup: np.array = None,
    config: dict = None
    ) -> dict:
    """transforms the image and thresholds the image"""
    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = image.copy()

    fidx = config.get("file",{}).get("id", -1)
    logger.info("File IDX: %s", fidx)

    img_shape = image.shape
    h = img_shape[0]
    w = img_shape[1]
    if len(img_shape) > 2:
        c = img_shape[2]
        logger.debug("PPI: W:%s H:%s C:%s", w, h, c)
    else:
        logger.debug("PPI: W:%s H:%s", w, h)

    save_steps = config.get("debug", {}).get("save")
    if save_steps:
        logger.debug("Saving Images...")

    if "contours" not in config:
        config["contours"] = {
            "mode": cv2.RETR_TREE,
            "method": cv2.CHAIN_APPROX_SIMPLE
        }

    # get some kernels to use...
    kernel_size = config.get("kernel",{}).get("size", 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

    # perform the base processing of the image...
    img_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

    if save_steps:
        cv2.imwrite(f'data/eng/F{fidx}.cc.gray.png', img_gray)

    thres_min = config.get("threshold", {}).get("thresh", 75)
    thres_max = config.get("threshold", {}).get("maxval", 255)
    thres_type = config.get("threshold", {}).get("type", cv2.THRESH_BINARY)
    _, img_thresh = cv2.threshold(src=img_gray, thresh=thres_min, maxval=thres_max, type=thres_type)

    if save_steps:
        cv2.imwrite(f'data/eng/F{fidx}.cc.thres.png', img_thresh)

    return {
        "gray": img_gray,
        "thresh": img_thresh
    }

# new processing steps...
def classify_contours(image: np.array, markup: np.array = None,
    config: dict = None
    ) -> dict:
    """This will extract the contours from an image, then
    process the contours to return the following:
        shape = edge of the contour is mostly the same pixel
        text = the grouping of contours into potential letter
        sequences
    it will return:
        type
            bounding box
                contours
    """
    fidx = config.get("file",{}).get("id", -1)
    logger.info("File IDX: %s", fidx)

    save_steps = config.get("debug", {}).get("save")

    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = image.copy()

    img_shape = image.shape
    h = img_shape[0]
    w = img_shape[1]
    if len(img_shape) > 2:
        c = img_shape[2]
        logger.debug("CCC: W:%s H:%s C:%s", w, h, c)
    else:
        logger.debug("CCC: W:%s H:%s", w, h)

    # process the image...
    contours, hierarchy = cv2.findContours(image=image, **config.get("contours"))
    cv2.drawContours(image=img_return, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1)

    # show the hierarchy
    for hidx, hval in enumerate(hierarchy):
        logger.info("\tH: %s => %s", hidx, hval)

    # prep the image
    data = {
        "shapes": [],
        "text": [],
        "boxes": [],
        "image": None
    }

    shapes = ShapeGrouper()
    boxes = ShapeGrouper()

    # process the contours
    # 1 operations
    #   Determine box
    #   Determine Shape
    for cidx, c in enumerate(contours):
        (bbx,bby,bbw,bbh) = cv2.boundingRect(c)
        rect = Rectangle(bbx,bby,bbw,bbh)
        rect.add_tags(contours=c, cidx=cidx)

        # smoot hteh contour to
        isopen = False
        peri = cv2.arcLength(c, isopen)
        if peri > 100:
            peri = 100.0
        approx = cv2.approxPolyDP(c, 0.04 * peri, isopen)
        shapes.add_rectangle(rect=rect)

        minw = config.get("boxes", {}).get("minwidth", 10)
        minh = config.get("boxes", {}).get("minheight", 10)

        # draw the approx shape...
        if len(approx) == 4 and bbw > minw and bbh > minh:
            # draw the bb corners...
            cv2.circle(img=img_return, center=(bbx, bby),
                    radius=(5), color=(255,0,255), thickness=1)
            cv2.circle(img=img_return, center=(bbx, bby),
                    radius=(10), color=(255,0,255), thickness=1)
            cv2.rectangle(img=img_return, pt1=(bbx, bby),
                    pt2=(bbx + bbw, bby + bbh), color=(255, 0, 255), thickness=1)

            # potential box so put into box list...
            rect.add_tags(isbox=True)
            boxes.add_rectangle(rect=rect)

        elif len(approx) > 4:
            cv2.drawContours(img_return, [approx], -1, (0,255,255), 1)
        else:
            cv2.drawContours(img_return, [approx], -1, (0,0,255), 1)

    if save_steps:
        logger.info("Shapes: {%s}", fidx)
        printTree(shapes.shapes)
        logger.info("Boxes: {%s}", fidx)
        printTree(obj=boxes.shapes)

        cv2.imwrite(f'data/eng/F{fidx}.cc.box.png', img_return)

    data["boxes"] = boxes
    data["shapes"] = shapes
    data["image"] = img_return
    return data

def classify_circles(image: np.array, markup: np.array = None,
    config: dict = None
    ) -> dict:
    """Used hough circles to find and highlight circles
    uses a gray scale image"""
    fidx = config.get("file",{}).get("id", -1)
    logger.info("File IDX: %s", fidx)

    save_steps = config.get("debug", {}).get("save")

    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = image.copy()

    shapes = ShapeGrouper()

    # now to extract circles
    method = config.get("circles", {}).get("method", cv2.HOUGH_GRADIENT)
    dp = config.get("circles", {}).get("dp", 1.2)
    mindist = config.get("circles", {}).get("mindist", 50)
    circles = cv2.HoughCircles(image=image, method=method, dp=dp, minDist=mindist)

    if circles is not None:
        # we have circles
        circles = np.round(circles[0, :]).astype("int")

        # iterate and show the circles
        for (x, y, r) in circles:
            cv2.circle(img_return, (x,y), r, (255,255,0), 1)
            rect = Rectangle(x=x-r, y=y-r, w=2*r, h=2*r)
            rect.add_tags(shape="circle", point=(x,y), radius=r)

    if save_steps:
        cv2.imwrite(f'data/eng/F{fidx}.cc.circles.png', img_return)

    return {"shapes": shapes}

def extract_artifacts(image: np.array, config: dict = None) -> dict:
    """The heavy lift function for documents
    will try to extract the following:
        grids: connected boxes
        text: text and it's position
    """
    fidx = config.get("file",{}).get("id", -1)
    logger.info("File IDX: %s", fidx)

    save_steps = config.get("debug", {}).get("save")
    if save_steps:
        logger.debug("Saving Images...")

    # pre process the image...
    image_data = process_image(image=image, config=config)

    # get the shapes (any contour)
    # get the boxes A contour whose approx length is 4
    img_gray = image_data.get("gray")
    img_thresh = image_data.get("thresh")

    # process the shapes
    cc_data = classify_contours(image=img_thresh, config=config)

    # process for circles if required...
    if config.get("operations", {}).get("circles", False):
        cc_circles = classify_circles(image=img_gray, config=config)

    # now build the grid and tables...


def process_alignments(image: np.array, markup: np.array = None,
    config: dict = None, baselines:dict=None, data: dict=None):
    """this process will group the contorurs into blocks...
    find the horizontal related contours...
        baselines = {
            "x": {},
            "y": {}
        }
    """
    if markup is not None:
        img_return = markup.copy()
    else:
        img_return = image.copy()

    for ly, val in baselines.get("y",{}).items():
        contours = []
        rects = np.array((0,4), int)

        for cidx in val:
            if contour := data.get("shapes",{})[cidx]:
                r1 = Rectangle(contour.x, contour.y, contour.w, contour.h)
                #rects.append(r1)
                contours.append(contour)
                # check if the rectangle is close to an already seen one


                rects = np.append(rects,np.array([[contour.x, contour.y, contour.w, contour.h]]), axis=0)
                rects, _ = cv2.groupRectangles(rects, 0, 0.85)
                #mrg_rects = [merge(r1=r1, r2=r2) for r2 in rects if intersect(r1=r1,r2=r2, border=border)]
                #descrete_rects = [r2 for r2 in rects if not intersect(r1=r1, r2=r2, border=border)]
                #rects = mrg_rects + descrete_rects

        # merge shapes together...
        #mrg_rects = [merge(r1=r1, r2=r2) for r2 in rects if intersect(r1=r1,r2=r2, border=border)]
        #descrete_rects = [r2 for r2 in rects if not intersect(r1=r1, r2=r2, border=border)]
        #rects = mrg_rects + descrete_rects

        #cv2.line(img=img_return, pt1=(minx,ly), pt2=(maxx,ly), color=(255, 255, 0), thickness=1)
        #for r1 in rects:
        for r in rects:
            cv2.putText(img=img_return, text=str(r), org=(5,ly), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 0), thickness=1)
            r1 = Rectangle(r[0], r[1], r[2], r[3])
            cv2.rectangle(img=img_return, pt1=(r1.x,r1.y), pt2=(r1.x+r1.w, r1.y+r1.h), color=(255, 255, 0), thickness=1)

    # find the vertical related contours...
    #for lx, val in baselines.get("x",{}).items():
    #    miny = h
    #    maxy = 0
    #    contours = []
    #    ys = set()
    #    for cidx in val:
    #        if contour := data.get("shapes",{})[cidx]:
    #            contours.append(contour)
    #            ys.add(contour.y)
    #            ys.add(contour.y + contour.h)
    #            maxy = max(contour.y + contour.h, maxy)
    #            miny = min(contour.y, miny)
    #
    #    cv2.line(img=img_return, pt1=(lx,miny), pt2=(lx,maxy), color=(255, 0, 255), thickness=1)
    #    # group by proximity....
    #    for yp in ys:
    #        cv2.line(img=img_return, pt1=(lx,yp), pt2=(lx,yp+5), color=(255, 0, 255), thickness=1)


    # add the markedup imag to the return
    #data["grid"] =
    data["image"] = img_return
    return data
