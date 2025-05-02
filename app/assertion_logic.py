from app.utils import generate_assertions_from_schema

def generate_basic_assertions(op_data):
    """
    Generates both positive and negative assertions for a given API operation.
    """
    assertions = []
    responses = op_data.get("responses", {})

    # ✅ Positive assertions
    for status_code in ["200", "201", "202"]:
        if status_code in responses:
            assertions.append(f"pm.response.to.have.status({status_code})")
            content = responses[status_code].get("content", {})
            json_schema = content.get("application/json", {}).get("schema", {})
            assertions += generate_assertions_from_schema(json_schema)

    # ❌ Negative assertions
    for status_code in ["400", "401", "403", "404", "409", "422", "500"]:
        if status_code in responses:
            assertions.append(f"pm.response.to.have.status({status_code})")
            # Check for message or error field in expected schema
            content = responses[status_code].get("content", {})
            json_schema = content.get("application/json", {}).get("schema", {})
            error_asserts = generate_assertions_from_schema(json_schema)
            if error_asserts:
                assertions += error_asserts
            else:
                # Fallback generic error message assertion
                assertions.append("pm.expect(pm.response.text()).to.include('error')")

    return assertions
