class NegativeTestGenerator:
    """
    Generates negative test cases based on Swagger/OpenAPI specifications.
    Focus: Invalid payloads, missing fields, wrong data types, etc.
    """

    def __init__(self, swagger_data):
        """
        Initialize with parsed Swagger/OpenAPI spec.
        """
        self.swagger_data = swagger_data

    def generate_negative_tests_for_endpoint(self, endpoint, method_details):
        """
        Generate negative test cases for a given endpoint and method.

        Args:
            endpoint (str): API path like '/user/login'
            method_details (dict): Details about POST/GET/PUT operation

        Returns:
            list: List of negative test case dictionaries
        """
        negative_tests = []

        # Step 1: Invalid payload structure (missing required fields)
        negative_tests += self._missing_required_fields(endpoint, method_details)
        
        # Step 2: Wrong data types
        negative_tests += self._wrong_data_types(endpoint, method_details)

        return negative_tests

    def _missing_required_fields(self, endpoint, method_details):
        """
        Generate test where required fields are missing.
        Handles both top-level and nested fields.
        """
        required_fields = method_details.get("required", [])
        schema = method_details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})

        negative_tests = []

        def handle_missing_fields(payload, required_fields):
            for field in required_fields:
                # Check for nested fields like 'user.address.city'
                field_parts = field.split('.')
                temp_payload = payload
                for part in field_parts:
                    if part not in temp_payload:
                        break
                    temp_payload = temp_payload[part]
                else:
                    # Recurse through nested objects and generate negative tests
                    neg_payload = payload.copy()
                    nested_payload = neg_payload
                    for part in field_parts[:-1]:
                        nested_payload = nested_payload.get(part, {})
                    nested_payload.pop(field_parts[-1], None)
                    negative_tests.append(neg_payload)

        # Initial empty payload
        initial_payload = self._generate_payload_from_schema(schema)
        handle_missing_fields(initial_payload, required_fields)

        return negative_tests

    def _wrong_data_types(self, endpoint, method_details):
        """
        Generate test where fields have wrong data types.
        """
        schema = method_details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
        properties = schema.get("properties", {})

        negative_tests = []

        def handle_wrong_data_types(payload, properties):
            for field, field_details in properties.items():
                field_type = field_details.get("type", "")
                wrong_type_value = self._get_wrong_data_for_type(field_type)
                if wrong_type_value is not None:
                    neg_payload = payload.copy()
                    neg_payload[field] = wrong_type_value
                    negative_tests.append(neg_payload)

        # Initial empty payload
        initial_payload = self._generate_payload_from_schema(schema)
        handle_wrong_data_types(initial_payload, properties)

        return negative_tests

    def _generate_payload_from_schema(self, schema):
        """
        Generate an empty payload based on the schema (handles different data types).
        """
        payload = {}
        properties = schema.get("properties", {})

        for field, field_details in properties.items():
            field_type = field_details.get("type", "")
            if field_type == "string":
                payload[field] = ""
            elif field_type == "integer":
                payload[field] = 0
            elif field_type == "boolean":
                payload[field] = False
            elif field_type == "array":
                payload[field] = []
            elif field_type == "object":
                payload[field] = {}
        return payload

    def _get_wrong_data_for_type(self, field_type):
        """
        Get a wrong data type value based on the field's expected type.
        """
        if field_type == "string":
            return 123  # wrong type for string
        elif field_type == "integer":
            return "string_value"  # wrong type for integer
        elif field_type == "boolean":
            return "string"  # wrong type for boolean
        elif field_type == "array":
            return {}  # wrong type for array
        elif field_type == "object":
            return "string_instead_of_object"  # wrong type for object
        return None
