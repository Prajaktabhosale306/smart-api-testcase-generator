from app.assertion_logic import build_negative_assertions
from app.payload_builder import generate_negative_payload
from app.nlp_summary import generate_test_summary
from app.descriptions import generate_test_case_summary

class NegativeTestGenerator:
    def __init__(self, swagger_spec, use_premium_nlp=False, use_nlp_summary=False):
        self.swagger_spec = swagger_spec
        self.use_premium_nlp = use_premium_nlp
        self.use_nlp_summary = use_nlp_summary

    def generate_negative_tests(self):
        negative_tests = []

        for path, path_data in self.swagger_spec.get("paths", {}).items():
            for operation, op_data in path_data.items():
                if operation.lower() in ["get", "post", "put", "delete"]:
                    test_case = self.create_negative_test_case(path, operation, op_data)
                    negative_tests.append(test_case)

        return negative_tests

    def create_negative_test_case(self, path, operation, op_data):
        test_case = {
            "path": path,
            "operation": operation,
            "parameters": op_data.get("parameters", []),
            "responses": op_data.get("responses", {})
        }

        # Generate invalid/missing/malformed payload
        test_case["request_payload"] = generate_negative_payload(op_data)

        # Summary (NLP or rule-based)
        base_summary = op_data.get("summary", "")
        if self.use_nlp_summary:
            # Use the new `generate_test_summary` for NLP-based summary
            test_case["summary"] = generate_test_summary(f"Negative test for {base_summary}", path, operation, premium=self.use_premium_nlp)
        else:
            # Fallback to rule-based summary
            test_case["summary"] = generate_test_case_summary(test_case, is_negative=True)

        # Assertions (like status code 400, expected error message, etc.)
        test_case["assertions"] = build_negative_assertions(op_data)

        return test_case
