from dataclasses import fields


def filter_fields(dataclass_type, input_dict):
    dataclass_fields = {f.name for f in fields(dataclass_type)}
    return {k: v for k, v in input_dict.items() if k in dataclass_fields}
