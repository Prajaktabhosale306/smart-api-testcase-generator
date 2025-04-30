def generate_assertions_from_schema(schema: dict) -> list:
    """
    Generate Postman-style assertions based on OpenAPI response schema.
    Supports type checks, required fields, and enum value validations.
    """
    assertions = []
    if not schema:
        return assertions

    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for field, info in properties.items():
        # Assert field is present
        if field in required:
            assertions.append(f"pm.expect(response).to.have.property('{field}')")

        # Assert correct type
        field_type = info.get("type")
        type_map = {
            "string": "string",
            "integer": "number",
            "number": "number",
            "boolean": "boolean",
            "array": "array",
            "object": "object"
        }
        if field_type in type_map:
            assertions.append(f"pm.expect(response.{field}).to.be.a('{type_map[field_type]}')")

        # Assert enum values
        if "enum" in info:
            enum_values = info["enum"]
            assertions.append(f"pm.expect(response.{field}).to.be.oneOf({enum_values})")

    return assertions
