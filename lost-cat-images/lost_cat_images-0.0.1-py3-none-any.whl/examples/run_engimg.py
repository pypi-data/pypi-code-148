from datetime import datetime
import logging
import glob
import re
import os

from lost_cat.utils.rules_utils import Rule, RuleEngine, RuleState, RulesTool
from lost_cat_images.parsers.engimg_parser import EngImgParser

logger = logging.getLogger(__name__)

def get_rules() -> RulesTool:
    """Returns the rules as RulesTool object"""
    rules = RulesTool()

    # tags
    rules.add_rule(Rule(
        name="tags",
        idx=1,
        engine=RuleEngine.REGEX, # ([A-Z]{1,3}[ -�]{1,3}[0-9]{2,4})
        expr="(?P<tag>[A-Z]{1,3}[ -�]{1,3}[0-9]{2,4})",
        tags=[{"key":"tag", "regex":"tag"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"findall":True}
    ))
    
    # Drawing Number
    rules.add_rule(Rule(
        name="drawing no",
        idx=1,
        engine=RuleEngine.REGEX, #([dwg|dwr|drawing]+[ no\.]{0,4})([0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})
        expr=r"(?P<dwg>[dwg|dwr|drawing]{0,1}[ no\.]{0,4})(?P<number>[0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})",
        tags=[{"key":"label", "regex":"tag"}, {"key": "number", "regex": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"findall":True, "flags": re.IGNORECASE}
    ))

    rules.add_rule(Rule(
        name="revision",
        idx=1,
        engine=RuleEngine.REGEX, #([dwg|dwr|drawing]+[ no\.]{0,4})([0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})
        expr=r"Rev[\. \-](?P<number>[0-9]+)",
        tags=[{"key":"revision", "regex":"number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"findall":True, "flags": re.IGNORECASE}
    ))

    return rules

def main(folderpath: str):
    """Loop through the found files and process
    save the results to a text file"""
    exts = []
    for src in EngImgParser.avail_config().get("source",[]):
        if src.get("key") == 'ext':
            exts = src.get("values")
            logger.info("Accept: %s", exts)

    # store the output...
    data = {}

    rules = get_rules()

    for fidx, fpath in enumerate(glob.glob(folderpath)):
        _, fname = os.path.split(fpath)
        filename, ext = os.path.splitext(fname)
        if ext.lower() in exts:
            if filename not in data:
                data[filename] = {
                    "fidx": fidx,
                    "path": fpath
                }
            data[filename]["blocks"] = process_file(uri=fpath, fidx=fidx)

    # now to extract the tags and other information
    for filename, value in data.items():
        fidx = value.get("fidx")
        txtname = f"data\{filename}_{fidx}.txt"
        with open(txtname, "w") as fp:
            logger.info("TAGS: {%s}", fidx)
            fp.write(f"File: {filename}\n")
            for bnum, bvalue in value.get("blocks",{}).items():
                fp.write(f"Block: {bnum}\n")
                logger.info("\t{%s}: Blocks: %s => %s\n", fidx, bnum, bvalue)
                phrases = []
                for pnum, text in bvalue.items():
                    phrase = ' '.join(text)
                    fp.write("\t{}\t{} => {}\n".format(fidx, pnum, phrase))
                    phrases.append(phrase)
                # 
                logger.info("\t{%s}: Phrases: %s", fidx, phrases)
                results = rules.run(phrases=phrases)
                logger.info("\t{%s}: Results: %s", fidx, results)

def process_file(uri:str, fidx:int = 0) -> dict:
    """run the initial parser against"""
    logger.info("process %s", uri)

    engobj = EngImgParser(uri)
    conf = engobj.get_config()
    if "parser" not in conf:
        conf["parser"] = {}
    if "file" not in conf.get("parser"):
        conf["parser"]["file"] = {}
    conf["parser"]["file"]["id"] = fidx
    if "debug" not in conf.get("parser"):
        conf["parser"]["debug"] = {}
    conf["parser"]["debug"]["save"] = True
    engobj.set_config(conf)

    funx = engobj.avail_functions().get("parser")
    data = funx()
    text_blocks = {}
    for key, value in data.items():
        logger.info("\t%s => %s", key, type(value))
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                logger.info("\t%s => %s", subkey, type(subvalue))
                if isinstance(subvalue, list):
                    for item in subvalue:
                        blocknum = item.get("idx")
                        paranum = item.get("par_num")
                        textarr = item.get("text")

                        if blocknum not in text_blocks:
                            text_blocks[blocknum] = {}
                        if paranum not in text_blocks.get(blocknum):
                            text_blocks[blocknum][paranum] = []
                        text_blocks[blocknum][paranum].append(textarr)

    # now to use the contour function
    #funx = engobj.avail_functions().get("contours")
    #cc_data = funx()

    engobj = None
    return text_blocks

if __name__ == "__main__":
    nb_name = "EngImg"
    if not os.path.exists("logs"):
        os.mkdir("logs")

    _logname = "{}.{}".format(nb_name, datetime.now().strftime("%Y%m%d"))
    logging.basicConfig(filename=f'logs\\log.{_logname}.log', level=logging.INFO)

    if not os.path.exists(r"data\eng\crops"):
        os.makedirs(r"data\eng\crops")

    fldrpath = r"F:\source\suncor\*" #r"data\*"
    main(folderpath=fldrpath)
