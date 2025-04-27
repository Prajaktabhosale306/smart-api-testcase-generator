# app/negative_test_generator.py

import copy

class NegativeTestGenerator:
    def __init__(self, swagger_loader):
        self.swagger_loader = swagger_loader

    def generate_negative_tests(self, method, method_details):
        negative_tests = []
        request_body = method_details.get("requestBody", {})
        content = request_body.get("content", {})
        schema = content.get("application/json", {}).get("schema", {})

        if not schema:
            return negative_tests  # No request body to generate negatives for

        resolved_schema = self.swagger_loader.resolve_ref(schema) if "$ref" in schema else schema
        required_fields = resolved_schema.get("required", [])
        properties = resolved_schema.get("properties", {})

        if not properties:
            return negative_tests

        base_payload = self._generate_payload_from_schema(resolved_schema)

        missing_required_payloads = self._handle_missing_required_fields(base_payload, required_fields)
        wrong_data_type_payloads = self._handle_wrong_data_types(base_payload, properties)

        negative_tests.extend(missing_required_payloads)
        negative_tests.extend(wrong_data_type_payloads)

        return negative_tests

    def _generate_payload_from_schema(self, schema):
        if "$ref" in schema:
            schema = self.swagger_loader.resolve_ref(schema)

        payload = {}
        properties = schema.get("properties", {})
        for field, details in properties.items():
            if "$ref" in details:
                details = self.swagger_loader.resolve_ref(details)

            field_type = details.get("type", "string")
            payload[field] = self._get_dummy_value(field_type)
        return payload

    def _get_dummy_value(self, field_type):
        dummy_values = {
            "string": "sample",
            "integer": 0,
            "number": 0.0,
            "boolean": True,
            "object": {},
            "array": []
        }
        return dummy_values.get(field_type, "sample")

    def _handle_missing_required_fields(self, payload, required_fields):
        negative_payloads = []
        for field in required_fields:
            modified_payload = copy.deepcopy(payload)
            if field in modified_payload:
                del modified_payload[field]
            negative_payloads.append({
                "type": "missing_required_field",
                "payload": modified_payload,
                "error_field": field
            })
        return negative_payloads

    def _handle_wrong_data_types(self, payload, properties):
        negative_payloads = []
        wrong_values = {
            "string": 123,
            "integer": "wrong_integer",
            "number": "wrong_number",
            "boolean": "not_boolean",
            "object": "not_an_object",
            "array": "not_an_array"
        }

        for field, details in properties.items():
            if "$ref" in details:
                details = self.swagger_loader.resolve_ref(details)

            correct_type = details.get("type", "string")
            if correct_type in wrong_values:
                modified_payload = copy.deepcopy(payload)
                modified_payload[field] = wrong_values[correct_type]
                negative_payloads.append({
                    "type": "wrong_data_type",
                    "payload": modified_payload,
                    "error_field": field
                })
        return negative_payloads
