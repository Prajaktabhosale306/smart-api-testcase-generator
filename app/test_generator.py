# app/test_generator.py
from app.negative_test_generator import NegativeTestGenerator
from app.assertion_logic import generate_basic_assertions


class TestGenerator:
    def __init__(self, swagger_loader):
        self.swagger_loader = swagger_loader
        self.swagger_spec = swagger_loader.swagger_data
        self.negative_generator = NegativeTestGenerator(self.swagger_spec)

    def generate_tests(self):
        """
        Generate all positive and negative test cases.
        """
        positive_tests = self.generate_positive_tests()
        negative_tests = self.negative_generator.generate_negative_tests()
        return positive_tests + negative_tests

    def generate_positive_tests(self):
        """
        Generate positive test cases based on Swagger data.
        """
        tests = []
        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation in ["get", "post", "put", "delete"]:
                    test_case = self.create_test_case(path, operation, op_data)
                    tests.append(test_case)
        return tests

    def create_test_case(self, path, operation, op_data):
        """
        Create a test case based on operation data from the Swagger specification.
        """
        test_case = {
            "path": path,
            "operation": operation,
            "summary": op_data.get("summary", ""),
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {}),
            "assertions": generate_basic_assertions(op_data)  # NEW line: Add basic assertions
        }
        return test_case
