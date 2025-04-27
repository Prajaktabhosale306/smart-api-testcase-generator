class NegativeTestGenerator:
    def __init__(self, swagger_spec):
        self.swagger_spec = swagger_spec

    def generate_negative_tests(self):
        """
        Generate negative test cases based on Swagger data.
        
        Returns:
            list: Negative test cases.
        """
        negative_tests = []
        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation in ["get", "post", "put", "delete"]:  # Operations we want to generate tests for
                    negative_test_case = self.create_negative_test_case(path, operation, op_data)
                    negative_tests.append(negative_test_case)
        return negative_tests

    def create_negative_test_case(self, path, operation, op_data):
        """
        Create a negative test case for the operation.
        
        Args:
            path (str): The API path.
            operation (str): HTTP operation (get, post, etc.).
            op_data (dict): Operation data from the Swagger spec.
        
        Returns:
            dict: A negative test case representation.
        """
        negative_test_case = {
            "path": path,
            "operation": operation,
            "summary": f"Negative test for {op_data.get('summary', '')}",
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {}),
            "expected_error": "400 Bad Request"  # Example negative test case
        }
        return negative_test_case
