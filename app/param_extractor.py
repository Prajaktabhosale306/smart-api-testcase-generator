# app/param_extractor.py

from typing import List, Dict, Any

def get_query_params(operation: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extracts query parameters from the operation's parameters.
    """
    params = operation.get("parameters", [])
    return [param for param in params if param.get("in") == "query"]
