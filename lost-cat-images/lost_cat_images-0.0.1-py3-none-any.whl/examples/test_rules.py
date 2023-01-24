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
    ridx = 0

    #  DRAWING NO. 5-2.235-001

    numstr = r"[0-9DOSB]+[\-\.�]+[0-9DOSB\-\.�]+[0-9DOSB]+"
    # tags
    ridx += 1
    rules.add_rule(Rule(
        name="tags",
        idx=ridx,
        engine=RuleEngine.REGEX, # ([A-Z]{1,3}[ -�]{1,3}[0-9]{2,4})
        expr="(?P<tag>[A-Z085]{2,5}[ -�]{1,2}[0-9SBDO]{3,10})", #[A-Z085]+[ -�]{1,3}[0-9SBDO]+)",
        tags=[{"key":"tag", "group":"tag"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"findall":True}
    ))

    ridx += 1
    rules.add_rule(Rule(
        name="drawing",
        idx=ridx,
        engine=RuleEngine.REGEX,
        expr=r".*(?P<number>" + numstr + ").*",
        tags=[{"key":"label", "value":"candidate"}, {"key": "number", "group": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))

    # Drawing Number
    ridx += 1
    rules.add_rule(Rule(
        name="drawing no",
        idx=ridx,
        engine=RuleEngine.REGEX, #([dwg|dwr|drawing]+[ no\.]{0,4})([0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})
        expr=r"(?P<label>[DO]{1}WG[ NO\.]+)(?P<number>" + numstr + ")",
        tags=[{"key":"label", "group":"label"}, {"key": "number", "group": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))
    ridx += 1
    rules.add_rule(Rule(
        name="drawing no",
        idx=ridx,
        engine=RuleEngine.REGEX, #([dwg|dwr|drawing]+[ no\.]{0,4})([0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})
        expr=r"(?P<label>[DO]{1}WR[ NO\.]+)(?P<number>" + numstr + ")",
        tags=[{"key":"label", "group":"label"}, {"key": "number", "group": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))
    ridx += 1
    rules.add_rule(Rule(
        name="drawing no",
        idx=ridx,
        engine=RuleEngine.REGEX, #([dwg|dwr|drawing]+[ no\.]{0,4})([0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})
        expr=r"(?P<label>DRAWING[ NO\.]+)(?P<number>{})$".format(numstr),
        tags=[{"key":"label", "group":"label"}, {"key": "number", "group": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))
    ridx += 1
    rules.add_rule(Rule(
        name="drawing no",
        idx=ridx,
        engine=RuleEngine.REGEX, #([dwg|dwr|drawing]+[ no\.]{0,4})([0-9]+[\-\.�]+[0-9\-\.�]+[0-9]{1})
        expr=r"(?P<label>[ NOno0\.]{3,4})(?P<number>" + numstr + ")",
        tags=[{"key":"label", "group":"label"}, {"key": "number", "group": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))
    ridx += 1
    rules.add_rule(Rule(
        name="drawing no",
        idx=ridx,
        engine=RuleEngine.REGEX, 
        expr=r"(?P<number>{})".format(numstr),
        tags=[{"key":"label", "value":"label"}, {"key": "number", "group": "number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))    

    ridx += 1
    rules.add_rule(Rule(
        name="revision",
        idx=ridx,
        engine=RuleEngine.REGEX, 
        expr=r".*Rev[\. \-](?P<number>[0-9OBDS]+).*",
        tags=[{"key":"revision", "group":"number"}],
        stop=False,
        state=RuleState.SINGLE,
        options={"flags": re.IGNORECASE}
    ))

    return rules

def get_phraseblocks():
    """Return a set of phrase to process"""
    phraseblocks = {}
    # INFO:__main__:	{0}: Phrases: [' <...> ']
    reg = re.compile(r".*\{(?P<fidx>[\d]+)\}:\sPhrases:\s\['(?P<phrase>.*)'\].*") #

    with open(r"logs\log.EngImg.20230123.log") as f:
        for line in f:
            if m:= reg.match(line.rstrip()):
                fidx = int(m.group("fidx"))
                phrase = m.group("phrase")
                logger.info("{%s}: %s", fidx,  phrase)

                if fidx not in phraseblocks:
                    phraseblocks[fidx] = []
                phraseblocks[fidx].append(phrase)
    
    return phraseblocks

def main():
    """Run the main thread"""
    rules = get_rules()
    phraseblocks = get_phraseblocks()
    
    logger.info("Rules:")
    for rule in rules.rules:
        logger.info("R: %s", rule.export())

    for fidx, phrases in phraseblocks.items():
        logger.info("fidx: %s", fidx)
        logger.debug("{%s}: Phrases: %s", fidx, phrases)
        metadata = {}

        for item in rules.run(phrases=phrases):
            logger.info("{%s}: Item: %s", fidx, item)
            rule = item.get("rule")
            result = item.get("result")

            if result.get("passed", False):
                logger.info("\tRule %s:%s => Tags: %s", rule.idx, rule.name, result.get("tags",{}))

            for tag, value in result.get("tags",{}).items():
                if tag not in metadata:
                    metadata[tag] = value
                else:
                    if value != metadata.get(tag):
                        if isinstance(metadata.get(tag), list):
                            metadata[tag].append(value)
                        else:
                            # handle converting to list
                            metadata[tag] = [metadata.get(tag), value]

        # show the results
        for tag,value in metadata.items():
            logger.info("{%s}: Tag: %s => %s", fidx, tag, value)


if __name__ == "__main__":
    nb_name = "TestRules"
    if not os.path.exists("logs"):
        os.mkdir("logs")

    _logname = "{}.{}".format(nb_name, datetime.now().strftime("%Y%m%d"))
    filename=f'logs\\log.{_logname}.log'
    if os.path.exists(filename):
        os.remove(filename)

    logging.basicConfig(filename=filename, level=logging.INFO)    
    main()