import json
from .negative_test_generator import NegativeTestGenerator  # Use relative import

class TestGenerator:
    def __init__(self, swagger_loader):
        self.swagger_loader = swagger_loader
        self.swagger_spec = swagger_loader.swagger_data
        self.negative_generator = NegativeTestGenerator(self.swagger_spec)

    def generate_tests(self):
        """
        Generate all positive and negative test cases.

        Returns:
            list: Combined test cases.
        """
        positive_tests = self.generate_positive_tests()
        negative_tests = self.negative_generator.generate_negative_tests()
        return positive_tests + negative_tests

    def generate_positive_tests(self):
        """
        Generate positive test cases based on Swagger data.
        
        Returns:
            list: Positive test cases.
        """
        tests = []
        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation in ["get", "post", "put", "delete"]:  # Operations we want to generate tests for
                    test_case = self.create_test_case(path, operation, op_data)
                    tests.append(test_case)
        return tests

    def create_test_case(self, path, operation, op_data):
        """
        Create a test case based on operation data from the Swagger specification.
        
        Args:
            path (str): The API path.
            operation (str): HTTP operation (get, post, etc.).
            op_data (dict): Operation data from the Swagger spec.
        
        Returns:
            dict: A test case representation.
        """
        test_case = {
            "path": path,
            "operation": operation,
            "summary": op_data.get("summary", ""),
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {})
        }
        return test_case
