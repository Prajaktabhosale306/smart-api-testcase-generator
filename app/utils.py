def extract_required_fields(parameters):
    required_fields = []
    payload = {}
    for param in parameters:
        if param.get("required") and param.get("in") in ["query", "body"]:
            required_fields.append(param["name"])
            payload[param["name"]] = f"sample_{param['name']}"
    return required_fields, payload

