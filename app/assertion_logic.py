def assert_status_code(response, expected_status=200):
    """Assert that the response status code matches the expected one."""
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

def assert_response_contains_keys(response_json, expected_keys):
    """Assert that certain keys exist in the response JSON."""
    missing_keys = [key for key in expected_keys if key not in response_json]
    assert not missing_keys, f"Missing keys in response: {missing_keys}"

def assert_field_value(response_json, field_name, expected_value):
    """Assert that a specific field has an expected value."""
    actual_value = response_json.get(field_name, None)
    assert actual_value == expected_value, f"Expected {field_name} to be {expected_value}, but got {actual_value}"

def assert_field_type(response_json, field_name, expected_type):
    """Assert that a specific field has the expected type."""
    if field_name not in response_json:
        raise AssertionError(f"Field '{field_name}' not found in response.")
    actual_type = type(response_json[field_name])
    assert actual_type == expected_type, f"Expected type {expected_type} for field '{field_name}', got {actual_type}"

# (Optional) More generic assertion functions can be added here later...
