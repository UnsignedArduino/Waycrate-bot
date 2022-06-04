TRUE = (
    "true",
    "t",
    "yes",
    "y",
    "1",
    "one"
)

FALSE = (
    "false",
    "f",
    "no",
    "0",
    "zero",
    None
)

TIME_NAME_ALIASES = {
    ("s", "sec", "secs", "second", "seconds"): "second",
    ("m", "min", "mins", "minute", "minutes"): "minute",
    ("h", "hr", "hrs", "hour", "hours"): "hour",
    ("d", "day", "days"): "day"
}

TIMES = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 86400
}


def boolean_parse(text: str) -> bool:
    t = text.lower().strip()
    if t in TRUE:
        return True
    elif t in FALSE:
        return False
    else:
        raise ValueError(f"Unknown boolean value for \"{text}\"")


def time_parse(text: str) -> float:
    t = text.lower().strip()
    for i, char in enumerate(t):
        if not char.isnumeric() and char not in (".", "-"):
            first_char_idx = i
            break
    else:
        raise ValueError(f"Ambiguous amount of time in string \"{text}\"")
    number_part = float(t[:first_char_idx].strip())
    type_part = t[first_char_idx:].strip()
    for aliases, name in TIME_NAME_ALIASES.items():
        if type_part in aliases:
            type_multiplier = TIMES[name]
            break
    else:
        raise ValueError(f"Unknown amount of seconds in \"{type_part}\" "
                         f"in string \"{text}\"")
    return number_part * type_multiplier


def aip(value: int, plural: str = "s", singular: str = "") -> str:
    return singular if value == 1 else plural
