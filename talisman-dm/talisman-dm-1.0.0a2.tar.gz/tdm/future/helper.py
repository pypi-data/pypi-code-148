from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, Union


def unfold_union(type_: type) -> Tuple[type, ...]:
    # check if it is union
    if hasattr(type_, '__origin__') and type_.__origin__ is Union:
        return type_.__args__
    return type_,


def is_subclass(type_: type, base_type: type) -> bool:
    try:
        return all(issubclass(t, base_type) for t in unfold_union(type_))
    except TypeError:
        return False  # here we should think about List[base_type] and others


def cache_result(key_param: Optional[str] = None, cache: Optional[dict] = None):
    if cache is None:
        cache = {}

    def wrap(f: Callable):
        def wrapper(*args, **kwargs) -> Any:
            if key_param is not None:
                key = kwargs[key_param]
            elif args:
                key = args[0]
            else:
                key = kwargs[next(iter(kwargs))]
            if key in cache:
                return cache[key]
            result = f(*args, **kwargs)
            cache[key] = result
            return result

        return wrapper

    return wrap


def generics_mapping(type_: type) -> Dict[TypeVar, type]:
    if issubclass(type_, Generic):  # actually it works (should be rewritten in more pythonic way)
        # assume type vars are not intersect
        result = {}
        for orig_base in type_.__orig_bases__:
            if '__origin__' in orig_base.__dict__ and '__args__' in orig_base.__dict__:
                result.update(dict(zip(orig_base.__origin__.__parameters__, orig_base.__args__)))
        return result
    return {}
