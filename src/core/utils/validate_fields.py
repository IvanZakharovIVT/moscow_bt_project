from typing import Any


def validate_spaces_str_field(field: Any) -> str:
    if isinstance(field, str):
        if field.strip() == "":
            raise ValueError("Входная строка не может быть пустой")
    return field