def build_payload_from_schema(schema):
    if not schema:
        return {}

    schema_type = schema.get('type', 'object')

    # 👉 Handle array at root level
    if schema_type == "array":
        item_schema = schema.get("items", {})
        return [build_payload_from_schema(item_schema)]

    if schema_type != 'object' or 'properties' not in schema:
        return {}

    payload = {}
    for prop, prop_schema in schema['properties'].items():
        prop_type = prop_schema.get("type", "string")

        if prop_type == "string":
            payload[prop] = "example_string"
        elif prop_type == "integer":
            payload[prop] = 123
        elif prop_type == "boolean":
            payload[prop] = True
        elif prop_type == "array":
            item_type = prop_schema.get("items", {}).get("type", "string")
            payload[prop] = ["item1", "item2"] if item_type == "string" else [1, 2]
        elif prop_type == "object":
            payload[prop] = {"example": "nested"}
        else:
            payload[prop] = None

    return payload
