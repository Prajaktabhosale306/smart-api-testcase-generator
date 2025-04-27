# negative_test_generator.py

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

        # Step 1: Invalid payload structure
        negative_tests.append(self._missing_required_fields(endpoint, method_details))
        
        # Step 2: Wrong data types
        negative_tests.append(self._wrong_data_types(endpoint, method_details))

        return negative_tests

    def _missing_required_fields(self, endpoint, method_details):
        """
        Generate test where required fields are missing.
        """
        # Pseudocode:
        # 1. Identify required fields from method_details
        # 2. Generate payload missing some required fields
        return {
            "test_name": f"Missing required fields for {endpoint}",
            "payload": {},  # we'll build a smart payload here
            "expected_status": 400  # Bad Request typically
        }

    def _wrong_data_types(self, endpoint, method_details):
        """
        Generate test where fields have wrong data types.
        """
        # Pseudocode:
        # 1. For each field, insert wrong type value
        return {
            "test_name": f"Wrong data types for {endpoint}",
            "payload": {},  # smart wrong payload here
            "expected_status": 400
        }
