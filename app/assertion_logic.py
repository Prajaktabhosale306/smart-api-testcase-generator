def generate_basic_assertions(op_data):
    """
    Generate basic assertion instructions for a given API operation based on Swagger/OpenAPI data.
    """
    assertions = []

    if "responses" in op_data:
        for expected_status in ["200", "201", "202", "204"]:
            if expected_status in op_data["responses"]:
                assertions.append({
                    "type": "status_code",
                    "expected": int(expected_status)
                })
                break

    return assertions
