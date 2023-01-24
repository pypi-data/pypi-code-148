import pandas as pd
from IPython.display import display


class CurvenoteStash(object):
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj

    def _repr_pretty_(self, pp, cycle):
        import json

        pp.text("")

    def _repr_mimebundle_(self, include, exclude):
        import json

        if isinstance(self.obj, pd.core.frame.DataFrame):
            try:
                ss = self.obj.reset_index().to_json(orient="records")
            except:
                ss = self.obj.reset_index(drop=True).to_json(orient="records")
            bundle = json.dumps({self.name: json.loads(ss)})
        else:
            bundle = json.dumps(self.obj)

        return {"application/vnd.curvenote.stash+json": bundle}


def stash(obj, name="stash"):
    display(CurvenoteStash(obj, name))
