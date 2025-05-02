# app/test_generator.py

from typing import List, Dict, Any
from app.swagger_loader import SwaggerLoader
from app.payload_builder import generate_payload
from app.param_extractor import get_query_params
from app.assertion_builder import (
    build_positive_assertions,
    build_negative_assertions
)
from app.utils import sanitize_test_case_name
from app.nlp_summary import generate_test_summary


def generate_test_cases(spec_input: Any) -> List[Dict[str, Any]]:
    """
    Main function to generate structured test cases from an OpenAPI spec.
    Returns a list of test case dicts.
    """
    # Use the SwaggerLoader class
    swagger_loader = SwaggerLoader(spec_input)
    spec = swagger_loader.spec  # This holds the loaded spec
    paths = swagger_loader.get_paths()  # This gets the 'paths' section of the spec

    test_cases = []

    for path, methods in paths.items():
        for method, operation in methods.items():
            operation_id = operation.get("operationId", f"{method}_{path}")
            summary = operation.get("summary", f"{method.upper()} {path}")

            # Payload generation
            request_body_schema = (
                operation.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )

            request_payload = generate_payload(request_body_schema, spec) if request_body_schema else {}

            # Query/path param extraction
            params = get_query_params(operation)

            # Assertions
            success_response = (
                operation.get("responses", {}).get("200") or
                operation.get("responses", {}).get("201") or
                operation.get("responses", {}).get("default")
            )
            response_schema = (
                success_response.get("content", {})
                .get("application/json", {})
                .get("schema", {})
                if success_response else {}
            )

            positive_asserts = build_positive_assertions(response_schema, spec)
            negative_asserts = build_negative_assertions(operation)

            # NLP-based test summary
            test_name = generate_test_summary({
                "method": method,
                "path": path,
                "params": params,
                "payload": request_payload
            })

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
