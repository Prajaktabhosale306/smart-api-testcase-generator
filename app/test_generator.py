from app.negative_test_generator import NegativeTestGenerator
class TestGenerator:
    def __init__(self, swagger_loader):
        self.swagger_loader = swagger_loader
        self.negative_generator = NegativeTestGenerator(swagger_loader)

    def generate_tests(self):
        endpoints = []

        for path, path_item in self.swagger_loader.paths.items():
            for method, method_details in path_item.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue  # skip unsupported methods

                endpoint_info = {
                    "endpoint": path,
                    "method": method.upper(),
                    "description": method_details.get("summary", ""),
                    "payload": {},
                    "required_fields": [],
                    "positive_test": {},
                    "negative_tests": []
                }

                # Generate payload for positive test
                request_body = method_details.get("requestBody", {})
                content = request_body.get("content", {})
                schema = content.get("application/json", {}).get("schema", {})

                if schema:
                    resolved_schema = self.swagger_loader.resolve_ref(schema) if "$ref" in schema else schema
                    endpoint_info["payload"] = self._generate_payload_from_schema(resolved_schema)
                    endpoint_info["required_fields"] = resolved_schema.get("required", [])
                    endpoint_info["positive_test"] = endpoint_info["payload"]

                # Prepare path and query parameters
                parameters = method_details.get("parameters", [])
                path_params = [p for p in parameters if p.get("in") == "path"]
                query_params = [p for p in parameters if p.get("in") == "query"]

                # Generate negative tests
                negative_tests = self.negative_generator.generate_negative_tests(
                    method,
                    method_details,
                    path_params=path_params,
                    query_params=query_params
                )
                endpoint_info["negative_tests"] = negative_tests

                endpoints.append(endpoint_info)

        return endpoints
