# common utils for all this
import json

def dict2cz(data: dict) -> str:
    # The dict will be nicely formatted
    dumped_dict = json.dumps(data, indent=4)
    # now do conversions like remove braces, etc
    cleaned = dumped_dict.replace(
        '\":',' ='
    ).replace(
        'false', 'no'
    ).replace(
        'true','yes'
    ).replace(
        '\"',''
    ).replace(
        ',',''
    )

    return cleaned
