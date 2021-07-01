def implicit_keys():
    codes = {"KEY": 1}
    return "KEY" in codes


def explicit_keys():
    codes = {"KEY": 1}
    return "KEY" in codes.keys()


def dict_values():
    codes = {"KEY": 1}
    return 1 in codes.values()


def return_dict_index_str(key: str):
    codes = {"KEY": 1}
    return codes[key]


def return_dict_index_int(key: int):
    codes = {1: "one"}
    return codes[key]


if __name__ == "__main__":
    assert implicit_keys()
    assert explicit_keys()
    assert dict_values()
    assert return_dict_index_str("KEY") == 1
    assert return_dict_index_int(1) == "one"
    print("OK")
