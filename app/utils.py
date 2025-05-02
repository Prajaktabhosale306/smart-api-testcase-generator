# app/utils.py

import re
from typing import Any, Dict, List

def resolve_ref(ref: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively resolve a $ref in the OpenAPI spec.
    """
    if not ref.startswith("#/"):
        raise ValueError(f"Unsupported ref format: {ref}")
    
    parts = ref.strip("#/").split("/")
    result = spec
    for part in parts:
        result = result.get(part)
        if result is None:
            raise KeyError(f"Unable to resolve reference: {ref}")
    
    if "$ref" in result:
        return resolve_ref(result["$ref"], spec)
    
    return result


def get_type_from_schema(schema: Dict[str, Any]) -> str:
    """
    Extracts type from schema including handling of $ref.
    """
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]
    elif "type" in schema:
        return schema["type"]
    elif "oneOf" in schema:
        return "oneOf"
    elif "anyOf" in schema:
        return "anyOf"
    elif "allOf" in schema:
        return "allOf"
    else:
        return "unknown"


def sanitize_test_case_name(text: str) -> str:
    """
    Converts a string into a safe test case ID or name.
    """
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'[^a-zA-Z0-9_]', '', text)
    return text.lower()


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flattens a nested dictionary into dot notation.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
