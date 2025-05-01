# Updated TestGenerator class with unified positive and negative test generation

from app.negative_test_generator import NegativeTestGenerator
from app.assertion_logic import generate_basic_assertions
from app.payload_generator import generate_payload, generate_negative_payload
from app.nlp_utils import generate_summary
from app.descriptions import generate_test_case_summary


class TestGenerator:
    def __init__(self, swagger_loader, use_premium_nlp=False, use_nlp_summary=False):
        self.swagger_loader = swagger_loader
        self.swagger_spec = swagger_loader.swagger_data
        self.negative_generator = NegativeTestGenerator(self.swagger_spec)
        self.use_premium_nlp = use_premium_nlp
        self.use_nlp_summary = use_nlp_summary

    def generate_tests(self):
        # Generate both positive and negative test cases
        positive_tests = self._generate_positive_tests()
        negative_tests = self._generate_negative_tests()
        return positive_tests + negative_tests

    def _generate_positive_tests(self):
        tests = []
        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation.lower() in ["get", "post", "put", "delete"]:
                    test_case = self._create_test_case(path, operation, op_data)
                    tests.append(test_case)
        return tests

    def _generate_negative_tests(self):
        tests = []
        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation.lower() in ["get", "post", "put", "delete"]:
                    test_case = self._create_negative_test_case(path, operation, op_data)
                    tests.append(test_case)
        return tests

    def _create_test_case(self, path, operation, op_data):
        test_case = {
            "path": path,
            "operation": operation,
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {}),
        }

        base_summary = op_data.get("summary", "")
        if self.use_nlp_summary:
            test_case["summary"] = generate_summary(base_summary, path, operation, premium=self.use_premium_nlp)
        else:
            test_case["summary"] = generate_test_case_summary(test_case)

        test_case["payload"] = generate_payload(op_data)
        test_case["assertions"] = generate_basic_assertions(op_data)

        return test_case

    def _create_negative_test_case(self, path, operation, op_data):
        test_case = {
            "path": path,
            "operation": operation,
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {}),
        }

        base_summary = f"Negative test case for {operation.upper()} {path} with invalid input"
        if self.use_nlp_summary:
            test_case["summary"] = generate_summary(base_summary, path, operation, premium=self.use_premium_nlp)
        else:
            test_case["summary"] = generate_test_case_summary(test_case)

        test_case["payload"] = generate_negative_payload(op_data)
        test_case["assertions"] = generate_basic_assertions(op_data, negative=True)

        return test_case

