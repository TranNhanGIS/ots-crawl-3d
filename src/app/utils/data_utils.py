"""
This module provides utility functions for converting data and vice versa.

Functions:
1. `is_valid_json`: Checks if a given string is valid JSON.
2. `str_to_json`: Converts a string to a Python object, either as a JSON or a Python literal.
3. `json_to_str`: Converts a Python object to a JSON string.
"""

import ast
import json


def is_valid_json(json_str: str) -> bool:
    """
    Checks if a string is a valid JSON by attempting to parse it.

    Args:
        json_str (str): The string to be checked.

    Returns:
        bool: True if the string is valid JSON, False otherwise.
    """
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


def str_to_json(json_str: str) -> json.JSONDecoder:
    """
    Converts a string to a Python object (either JSON or a Python literal).

    If the string is valid JSON, it will be parsed as JSON.
    If not, it will be evaluated as a Python literal expression using `ast.literal_eval`.

    Args:
        json_str (str): The string to be converted.

    Returns:
        json.JSONDecoder: The Python object (parsed JSON or evaluated Python literal).
    """
    if is_valid_json(json_str):
        return json.loads(json_str)
    else:
        return ast.literal_eval(json_str)


def json_to_str(obj: ast.AST) -> str:
    """
    Converts a Python object (AST) to a JSON string.

    Args:
        obj (ast.AST): The Python object to be converted.

    Returns:
        str: The string representation of the object in JSON format.
    """
    return json.dumps(obj)
