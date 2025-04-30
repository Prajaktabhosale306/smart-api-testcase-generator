from app.negative_test_generator import NegativeTestGenerator
from app.assertion_logic import generate_basic_assertions
from app.nlp_utils import generate_summary  # <-- New

class TestGenerator:
    def __init__(self, swagger_loader, use_premium_nlp=False):
        self.swagger_loader = swagger_loader
        self.swagger_spec = swagger_loader.swagger_data
        self.negative_generator = NegativeTestGenerator(self.swagger_spec)
        self.use_premium_nlp = use_premium_nlp

    def generate_tests(self):
        positive_tests = self.generate_positive_tests()
        negative_tests = self.negative_generator.generate_negative_tests()
        return positive_tests + negative_tests

    def generate_positive_tests(self):
        tests = []
        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation in ["get", "post", "put", "delete"]:
                    test_case = self.create_test_case(path, operation, op_data)
                    tests.append(test_case)
        return tests

    def create_test_case(self, path, operation, op_data):
        summary = op_data.get("summary", "")
        enriched_summary = generate_summary(summary, path, operation, premium=self.use_premium_nlp)
        return {
            "path": path,
            "operation": operation,
            "summary": enriched_summary,
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {}),
            "assertions": generate_basic_assertions(op_data)
        }
