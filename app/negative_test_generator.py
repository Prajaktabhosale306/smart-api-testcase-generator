# app/negative_test_generator.py

import copy

class NegativeTestGenerator:
    def __init__(self, swagger_loader):
        self.swagger_loader = swagger_loader

    def generate_negative_tests(self, method, method_details, path_params=None, query_params=None):
        negative_tests = []
        
        # Handle body-based negatives
        request_body = method_details.get("requestBody", {})
        content = request_body.get("content", {})
        schema = content.get("application/json", {}).get("schema", {})

        if schema:
            resolved_schema = self.swagger_loader.resolve_ref(schema) if "$ref" in schema else schema
            base_payload = self._generate_payload_from_schema(resolved_schema)
            required_fields = resolved_schema.get("required", [])
            properties = resolved_schema.get("properties", {})
            
            if properties:
                negative_tests.extend(self._handle_missing_required_fields(base_payload, required_fields))
                negative_tests.extend(self._handle_wrong_data_types(base_payload, properties, required_fields))

        # Handle query/path parameter negatives
        if path_params:
            negative_tests.extend(self._handle_missing_required_parameters(path_params, "path"))
        if query_params:
            negative_tests.extend(self._handle_missing_required_parameters(query_params, "query"))

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
            if field_type == "object" and "properties" in details:
                payload[field] = self._generate_payload_from_schema(details)
            else:
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
                "location": "body",
                "payload": modified_payload,
                "error_field": field
            })
        return negative_payloads

    def _handle_wrong_data_types(self, payload, properties, required_fields):
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
            if field in required_fields and correct_type in wrong_values:
                modified_payload = copy.deepcopy(payload)
                modified_payload[field] = wrong_values[correct_type]
                negative_payloads.append({
                    "type": "wrong_data_type",
                    "location": "body",
                    "payload": modified_payload,
                    "error_field": field
                })
        return negative_payloads

    def _handle_missing_required_parameters(self, parameters, location_type):
        negative_payloads = []
        for param in parameters:
            if param.get("required", False):
                payload = {p['name']: "sample" for p in parameters if p['required']}
                if param["name"] in payload:
                    del payload[param["name"]]
                negative_payloads.append({
                    "type": "missing_required_param",
                    "location": location_type,
                    "payload": payload,
                    "error_field": param["name"]
                })
        return negative_payloads
