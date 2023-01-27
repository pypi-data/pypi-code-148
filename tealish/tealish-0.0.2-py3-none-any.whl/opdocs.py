import json


lang_spec = json.load(open("/Users/fergal/Downloads/langspec.json"))
ops = {op["Name"]: op for op in lang_spec["Ops"]}

abc = "ABCDEFGHIJK"


def type_lookup(a):
    return {
        ".": "Any",
        "B": "bytes",
        "U": "int",
        "": "None",
    }[a]


docs = {}

fields = {}
fields["Global"] = list(
    zip(ops["global"]["ArgEnum"], map(type_lookup, ops["global"]["ArgEnumTypes"]))
)
fields["Txn"] = list(
    zip(ops["txn"]["ArgEnum"], map(type_lookup, ops["txn"]["ArgEnumTypes"]))
)
docs["fields"] = fields

docs["ops"] = {}

for op in ops.values():
    # print(op)
    name = op["Name"]
    immediate_args = op["Size"] - 1
    args = op.get("Args", "")
    arg_list = [f"{abc[i]}: {type_lookup(args[i])}" for i in range(len(args))]
    if "ArgEnum" in op:
        arg_list = ["F: field"] + arg_list
    elif immediate_args:
        arg_list = (["i: int"] * immediate_args) + arg_list
    arg_string = ", ".join(arg_list)
    returns = op.get("Returns", "")[::-1]
    ret = ", ".join([type_lookup(returns[i]) for i in range(len(returns))])
    sig = f"{op['Name']}({arg_string}) -> {ret}"

    docs["ops"][name] = {
        "sig": sig,
        "doc": op["Doc"],
        "doc_extra": op.get("DocExtra"),
        # 'fields': list(zip(op.get('ArgEnum', []), map(type_lookup, op.get('ArgEnumTypes', []))))
    }

json.dump(docs, open("/Users/fergal/Downloads/avmdocs.json", "w"), indent=2)
