from typing import Any, Dict, Callable
import json
import asyncio

def concat_dict(dict1, dict2):
    return {**dict1, **dict2}

def key_exists(dictionary, key):
    return key in dictionary

def value_exists(dictionary, value):
    return value in dictionary.values()

def clone(obj):
    if obj is None or type(obj) not in (dict, list):
        return obj
    if isinstance(obj, dict):
        copy = {}
        for key in obj:
            copy[key] = clone(obj[key])
        return copy
    elif isinstance(obj, list):
        copy = []
        for item in obj:
            copy.append(clone(item))
        return copy
    else:
        raise ValueError("Unable to copy object! Its type isn't supported.")


def is_empty(dictionary):
    return len(dictionary) == 0

def get_value_from_dict(dictionary, key_path):
    keys = key_path.split(".")
    val = dictionary

    for key in keys:
        if not isinstance(val, dict):
            return None
        val = val.get(key)
    return val


def is_subset(dict1, dict2):
    return all(item in dict2.items() for item in dict1.items())

def sort_dict_by_key(d):
    return dict(sorted(d.items()))



def sort_dict_by_custom_key(d: Dict, key_extractor: Callable[[Any, Any], Any]) -> dict:
    items = list(d.items())
    items.sort(key=lambda item: key_extractor(item[0], item[1]))
    return dict(items)

def pretty_print_dict(d: dict, indent=4) -> None:
    print(json.dumps(d, indent=indent))

def iterate_dict(d: dict):
    for k, v in d.items():
        yield k, v


async def clone_async(obj):
    if obj is None or type(obj) not in (dict, list):
        return obj
    if isinstance(obj, dict):
        copy = {}
        tasks = []
        for key in obj:
            tasks.append(asyncio.create_task(clone_async(obj[key])))
        results = await asyncio.gather(*tasks)
        for key, result in zip(obj.keys(), results):
            copy[key] = result
        return copy
    elif isinstance(obj, list):
        copy = []
        tasks = []
        for item in obj:
            tasks.append(asyncio.create_task(clone_async(item)))
        results = await asyncio.gather(*tasks)
        for result in results:
            copy.append(result)
        return copy
    else:
        raise ValueError("Unable to copy object! Its type isn't supported.")
