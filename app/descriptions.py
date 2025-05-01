def generate_human_readable_summary(test_case):
    """
    Generate a human-readable and dynamic summary for each test case.
    """
    operation = test_case.get("operation", "").upper()
    path = test_case.get("path", "")
    responses = test_case.get("responses", {})
    
    # Default response code and description
    response_code = responses.get("200", {}).get("description", "successful operation")
    
    # Optional parameters and query parameters
    parameters = test_case.get("parameters", [])
    optional_params = [param for param in parameters if param.get("required") is False]
    query_params = [param for param in parameters if param.get("in") == "query"]

    # Handle various types of operations dynamically
    if operation == "POST":
        # For POST requests, focus on creation or upload
        if "upload" in path.lower():
            summary = f"Validate that uploading the image to {path} is successful with status code 201. Ensure the image is uploaded correctly and the response includes the image URL."
        else:
            summary = f"Validate that creating a resource at {path} is successful with status code 201. Ensure the response body includes the created resource details, such as ID and other relevant attributes."
    elif operation == "GET":
        # For GET requests, focus on retrieving or finding a resource
        summary = f"Validate that retrieving data from {path} is successful with status code 200. Ensure the response body contains the expected data fields, including details about the resource."
    elif operation == "PUT":
        # For PUT requests, focus on updating a resource
        summary = f"Validate that updating the resource at {path} is successful with status code 200. Ensure that the updated resource is returned with the expected values."
    elif operation == "DELETE":
        # For DELETE requests, focus on deletion
        summary = f"Validate that deleting the resource at {path} is successful with status code 200. Ensure the resource is removed and no longer retrievable."
    else:
        # Default for other operations (PATCH, etc.)
        summary = f"Validate that the {operation} request to {path} returns a successful response."

    # Add contextual information for optional and query parameters
    if optional_params:
        optional_param_names = [param["name"] for param in optional_params]
        summary += f" Validate the handling of optional parameters: {', '.join(optional_param_names)}."
    
    if query_params:
        query_param_names = [param["name"] for param in query_params]
        summary += f" Validate filtering using query parameters: {', '.join(query_param_names)}."

    # Add more specific validation details if available
    if "schema" in responses.get("200", {}):
        schema = responses["200"]["schema"]
        if "$ref" in schema:
            summary += f" Ensure that the response schema references {schema['$ref']} and its attributes are validated."

    # Validate error cases, e.g., 4xx/5xx responses
    error_responses = [response for code, response in responses.items() if code.startswith("4") or code.startswith("5")]
    for error in error_responses:
        error_code = error.get("code", "Unknown error code")
        error_message = error.get("description", "An error occurred")
        summary += f" If the request fails, validate that the response includes a {error_code} status and the message '{error_message}'."

    # Additional context for specific validations (if any)
    if "validate" in path.lower():
        summary += " Ensure that all required validations are applied correctly."

    # Include performance check (optional, if needed)
    if "performance" in test_case:
        summary += " Ensure that the response time for this operation is within an acceptable range (e.g., < 2 seconds)."

    return summary
