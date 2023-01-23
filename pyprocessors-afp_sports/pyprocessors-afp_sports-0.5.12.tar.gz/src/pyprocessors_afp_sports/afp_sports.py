from collections import namedtuple, Counter
from functools import lru_cache
from pathlib import Path
from typing import Type, cast, List

import pandas as pd
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Category

logger = Logger("pymultirole")


class AFPSportsParameters(ProcessorParameters):
    as_altText: str = Field(
        "fingerprint2",
        description="""Name of the alternative text containing the fingerprint of the input document.""",
    )


class AFPSportsProcessor(ProcessorBase):
    """AFPSports processor ."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: AFPSportsParameters = cast(AFPSportsParameters, parameters)
        topics = get_mediatopics()
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if document.altTexts:
                    document.categories = document.categories or []
                    categories = {c.labelName: c for c in document.categories}
                    sports = []
                    fingers = [alt.text for alt in document.altTexts if alt.name == params.as_altText]
                    if fingers and len(fingers) > 0:
                        finger = fingers[0]
                        wikidatas = [t for t in finger.split() if t.startswith('Q')]
                        for qid in wikidatas:
                            if qid in topics:
                                sports.append(qid)
                    if sports:
                        counter = Counter(sports)
                        total = sum(counter.values())
                        for qid, count in counter.most_common():
                            cname = topics[qid].path
                            clabel = f"{cname.replace('_', '/')} ({topics[qid].label})"
                            score = count / total
                            if cname in categories:  # category already set by model, give it an higher score
                                categories[cname].score += score
                                categories[cname].properties = categories[cname].properties or {}
                            else:
                                categories[cname] = Category(labelName=cname, label=clabel, score=score, properties={})
                            categories[cname].properties["firedBy"] = qid
                    document.categories = list(categories.values())
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPSportsParameters


Mediatopic = namedtuple('Mediatopic', ['label', 'code', 'path'])


@lru_cache(maxsize=None)
def get_mediatopics(roots=['15000000_20000822_', '15000000_20001108_']):
    wikidata_prefix = "https://www.wikidata.org/entity/"
    iptc = Path(__file__).parent / "IPTC-MediaTopic-NewsCodes.xlsx"
    topics = {}
    iptc_codes = pd.read_excel(iptc, header=1).fillna(value="")
    levels = [None] * 6
    wikidata = None
    for index, row in iptc_codes.iterrows():
        topic_url = row['NewsCode-QCode (flat)']
        topic_code = topic_url[len('medtop:'):]
        wiki_mapping = row['Wikidata mapping']
        if wiki_mapping and wiki_mapping.startswith(wikidata_prefix):
            wikidata = wiki_mapping[len(wikidata_prefix):]
        for lev in range(0, 6):
            level = f"Level{lev + 1}/NewsCode"
            level_url = row[level]
            if level_url:
                level_code = level_url[len('medtop:'):]
                levels[lev] = level_code
                break
        path = '_'.join(levels[0:lev + 1])
        has_root = False
        for root in roots:
            if path.startswith(root):
                has_root = True
        if has_root and wikidata:
            topics[wikidata] = Mediatopic(label=row['Name (en-GB)'], code=topic_code,
                                          path=path)
    return topics
