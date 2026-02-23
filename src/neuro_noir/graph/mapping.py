from typing import Any


def flatten_prim(arg: Any) -> str | int | float:
    if isinstance(arg, (str, int, float)):
        return arg
    return str(arg)
    

def flatten_list(arg: Any) -> str | int | float | list[float | str | float]:
    if isinstance(arg, (str, int, float)):
        return arg
    if isinstance(arg, list) :
        return [ flatten_prim(item) for item in arg ]
    return str(arg)


def flatten_dict(d: dict) -> dict:
    return {k:flatten_list(v) for k,v in d.items()}