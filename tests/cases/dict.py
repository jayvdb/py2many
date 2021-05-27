def implicit_keys():
    CODES = {"KEY": 1}
    return "KEY" in CODES


def explicit_keys():
    CODES = {"KEY": 1}
    return "KEY" in CODES.keys()


def dict_values():
    CODES = {"KEY": 1}
    return 1 in CODES.values()


def return_dict_index_str(key: str):
    CODES = {"KEY": 1}
    return CODES[key]


def return_dict_index_int(key: int):
    CODES = {1: "one"}
    return CODES[key]

def dict_get():
    CODES = {"KEY": 1}
    assert CODES.get("KEY") == 1


def dict_get_default():
    CODES = {"KEY": 1}
    assert CODES.get("MISSING", 2) == 2


if __name__ == "__main__":
    assert implicit_keys()
    assert explicit_keys()
    assert dict_values()
    assert return_dict_index_str("KEY") == 1
    assert return_dict_index_int(1) == "one"
    dict_get()
    dict_get_default()
    print("OK")
