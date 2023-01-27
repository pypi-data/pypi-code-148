import json

from ukr.wfst import apply_fst_text, json_graph


def normalize(text: str) -> str:
    """
    Make ITN on the given text
    :param text: source text
    :return: normalized text
    """
    json_text = apply_fst_text(text, json_graph)
    json_tokens = json.loads(json_text)

    res = []
    for token, word in zip(json_tokens, text.split()):
        klass = next(iter(token.keys()))
        norm = next(iter(token.values()))

        # If we have from zero to nine - use spoken form
        if klass != 'word' and len(norm) == 1:
            res.append(word)
        else:
            res.append(word)

    return ' '.join(res)
