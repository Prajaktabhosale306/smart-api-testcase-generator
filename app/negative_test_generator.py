class NegativeTestGenerator:
    def __init__(self, swagger_data):
        self.swagger_data = swagger_data

    def generate_negative_tests_for_endpoint(self, endpoint, method_details):
        negative_tests = []
        
        # Step 1: Invalid payload structure (missing required fields)
        negative_tests += self._missing_required_fields(endpoint, method_details)
        
        # Step 2: Wrong data types
        negative_tests += self._wrong_data_types(endpoint, method_details)

        return negative_tests

    def _missing_required_fields(self, endpoint, method_details):
        required_fields = method_details.get("required", [])
        schema = method_details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})

        negative_tests = []

        if schema:
            # Generate negative tests where required fields are missing
            initial_payload = self._generate_payload_from_schema(schema)
            self._handle_missing_fields(initial_payload, required_fields, negative_tests)

        return negative_tests

    def _handle_missing_fields(self, payload, required_fields, negative_tests):
        """
        Recursively handle missing fields for nested structures.
        """
        for field in required_fields:
            field_parts = field.split('.')
            nested_payload = payload

            # Traverse through nested fields
            for part in field_parts[:-1]:
                nested_payload = nested_payload.get(part, {})
                if not isinstance(nested_payload, dict):
                    break
            else:
                # Remove the field from the payload if it's nested
                neg_payload = self._deep_copy(payload)
                nested_payload = neg_payload
                for part in field_parts[:-1]:
                    nested_payload = nested_payload.get(part, {})
                nested_payload.pop(field_parts[-1], None)
                negative_tests.append(neg_payload)

    def _wrong_data_types(self, endpoint, method_details):
        schema = method_details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
        properties = schema.get("properties", {})

        negative_tests = []

        if schema:
            # Generate test cases for wrong data types
            initial_payload = self._generate_payload_from_schema(schema)
            self._handle_wrong_data_types(initial_payload, properties, negative_tests)

        return negative_tests

    def _handle_wrong_data_types(self, payload, properties, negative_tests):
        """
        Handle wrong data type test cases.
        """
        for field, field_details in properties.items():
            field_type = field_details.get("type", "")
            wrong_type_value = self._get_wrong_data_for_type(field_type)
            if wrong_type_value is not None:
                # Modify the field with wrong data type
                neg_payload = self._deep_copy(payload)
                neg_payload[field] = wrong_type_value
                negative_tests.append(neg_payload)

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

    def _deep_copy(self, obj):
        """
        Perform a deep copy of the given object (used for nested objects).
        """
        import copy
        return copy.deepcopy(obj)
