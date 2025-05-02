# app/assertion_logic.py

def build_positive_assertions(response_schema: Dict[str, Any], spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Builds positive assertions based on the response schema.
    """
    # Example logic for positive assertions
    assertions = []
    if response_schema.get("type") == "object":
        assertions.append({
            "type": "status_code",
            "expected": 200
        })
    return assertions

def build_negative_assertions(operation: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Builds negative assertions for error cases in the operation.
    """
    # Example logic for negative assertions
    assertions = []
    error_responses = operation.get("responses", {}).get("default", {})
    if error_responses:
        assertions.append({
            "type": "status_code",
            "expected": 400
        })
    return assertions
