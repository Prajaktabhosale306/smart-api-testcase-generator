from typing import List, Dict, Any
from app.swagger_loader import SwaggerLoader
from app.payload_builder import generate_payload
from app.param_extractor import get_query_params
from app.assertion_logic import build_positive_assertions, build_negative_assertions
from app.utils import sanitize_test_case_name
from app.nlp_summary import generate_test_summary


class TestGenerator:
    def __init__(self, spec_input: Any):
        """
        Initializes the TestGenerator with the provided OpenAPI spec input.
        Accepts dict, URL, or file path.
        """
        self.swagger_loader = SwaggerLoader(spec_input)
        self.spec = self.swagger_loader.spec
        self.paths = self.swagger_loader.get_paths()

    def generate_test_cases(self) -> List[Dict[str, Any]]:
        test_cases = []

        for path, methods in self.paths.items():
            for method, operation in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue  # Skip unsupported methods

                operation_id = operation.get("operationId", f"{method}_{path}")
                summary = operation.get("summary", f"{method.upper()} {path}")

                # Request payload schema
                request_body_schema = (
                    operation.get("requestBody", {})
                    .get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
                )
                request_payload = generate_payload(request_body_schema, self.spec) if request_body_schema else {}

                # Extract query/path parameters
                params = get_query_params(operation)

                # Success response schema (200, 201, or default)
                responses = operation.get("responses", {})
                success_response = responses.get("200") or responses.get("201") or responses.get("default")
                response_schema = (
                    success_response.get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
                    if success_response else {}
                )

                # Generate assertions
                positive_asserts = build_positive_assertions(response_schema, self.spec)
                negative_asserts = build_negative_assertions(operation)

                # NLP-based test case summary
                test_name = generate_test_summary(
                    summary=operation.get("summary", f"{method.upper()} {path}"),
                    path=path,
                    operation=method,
                    premium=False  # Set to True for ChatGPT-based summary
                )

                # Final structured test case
                test_case = {
                    "name": sanitize_test_case_name(test_name),
                    "description": test_name,
                    "method": method.upper(),
                    "path": path,
                    "params": params,
                    "payload": request_payload,
                    "positive_assertions": positive_asserts,
                    "negative_assertions": negative_asserts,
                    "tags": operation.get("tags", [])
                }

                test_cases.append(test_case)

        return test_cases
