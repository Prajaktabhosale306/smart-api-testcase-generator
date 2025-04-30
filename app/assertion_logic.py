from app.utils import generate_assertions_from_schema

def generate_basic_assertions(op_data):
    """
    Generates basic + schema-based assertions for a given operation.
    """
    assertions = []

    # ✅ Always check status 200 if it exists
    responses = op_data.get("responses", {})
    if "200" in responses:
        assertions.append("pm.response.to.have.status(200)")
        content = responses["200"].get("content", {})
        json_schema = content.get("application/json", {}).get("schema", {})

        # 🔍 Add assertions from response schema
        assertions += generate_assertions_from_schema(json_schema)

    return assertions
