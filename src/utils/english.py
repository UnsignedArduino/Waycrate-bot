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


def boolean_parse(text: str) -> bool:
    t = text.lower()
    if t in TRUE:
        return True
    elif t in FALSE:
        return False
    else:
        raise ValueError(f"Unknown boolean value for: \"{text}\"")


def aip(value: int, plural: str = "s", singular: str = "") -> str:
    return singular if value == 1 else plural
