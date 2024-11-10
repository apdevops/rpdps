import pytest
import time
from library.api_helper import APIHelper


BASE_URL = "https://mockapi.rapidextras.com/login"

# Define test data in TDD format
test_data = [
    {
        "name": "valid_credentials",
        "payload": {"username": "validuser@example.com", "password": "validuser@example.com"},
        "expected_status": 200,
        "expected_token": True,
        "expected_error": None,
        "expected_headers": {"Content-Type": "application/json; charset=utf-8"},
        "response_time": 2,
    },
    {
        "name": "invalid_username",
        "payload": {"username": "invaliduser@example.com", "password": "validuser@example.com"},
        "expected_status": 401,
        "expected_token": False,
        "expected_blank_json": True
    },
    {
        "name": "invalid_password",
        "payload": {"username": "validuser@example.com", "password": "invaliduser@example.com"},
        "expected_status": 400,
        "expected_token": False,
        "expected_error": "invalid email address."
    },
    {
        "name": "empty_username",
        "payload": {"username": "", "password": "validuser@example.com"},
        "expected_status": 400,
        "expected_token": False,
        "expected_error": "username and password are required.",
    },
    {
        "name": "empty_password",
        "payload": {"username": "validuser@example.com", "password": ""},
        "expected_status": 400,
        "expected_token": False,
        "expected_error": "username and password are required.",
    },
    {
        "name": "long_username",
        "payload": {"username": "validuser@example.com" * 1000, "password": "validuser@example.com"},
        "expected_status": 400,
        "expected_token": False,
        "expected_error": "invalid email address.",
    },
    {
        "name": "special_characters_in_username",
        "payload": {"username": "admin$%", "password": "validuser@example.com"},
        "expected_status": 400,
        "expected_token": False,
        "expected_error": "invalid email address.",
    },
    {
        "name": "malformed_json_response",
        "payload": {"username": "malformeduser@example.com", "password": "malformeduser@example.com"},
        "expected_status": 200,  # Assume the server response with 200 but malformed JSON
        "expected_token": False,
        "expected_malformed_json": True,
    },
    {
        "name": "server_error",
        "payload": {"username": "erroruser@example.com", "password": "erroruser@example.com"},
        "expected_status": 500,
        "expected_token": False,
        "expected_blank_json": True
    },
    {
        "name": "slow_response",
        "payload": {"username": "slowuser@example.com", "password": "slowuser@example.com"},
        "expected_status": 200,
        "expected_token": True,
        "expected_delay": 2,  # Expect delay of 2 seconds or more
    }
]


@pytest.mark.parametrize("data", test_data, ids=[td["name"] for td in test_data])
def test_login_api(data):
    time.sleep(2) # wait between requests
    response, response_time = APIHelper.send_post_request(BASE_URL, data["payload"])

    # Validate status code
    assert response.status_code == data["expected_status"], f"Expected status {data['expected_status']} but got {response.status_code}"

    # Check for blank JSON response, if specified
    if data.get("expected_blank_json"):
        if response.text.strip() == "":  # Check if response body is empty
            assert True, "Received expected blank JSON response"
        else:
            try:
                json_data = response.json()
                assert json_data == {}, "Expected a blank JSON response, but got non-empty JSON"
            except ValueError:
                assert False, "Expected a blank JSON response, but got a non-JSON response"
    elif data.get("expected_malformed_json"):
        # Check if response is malformed JSON, if specified
        try:
            response.json()  # Attempt to parse JSON
            assert False, "Expected malformed JSON response"
        except ValueError:
            assert True  # Pass if ValueError is raised

    else:
        # Validate token presence or absence in response body
        if data["expected_token"]:
            assert "token" in response.json(), "Token should be present in response"
        else:
            assert "token" not in response.json(), "Token should not be present in response"

    # Validate error message in response body
    if data.get("expected_error"):
        assert data["expected_error"].lower() in response.json().get("error", "").lower(), f"Expected error message: {data['expected_error']}"

    # Validate headers
    if "expected_headers" in data:
        for header, expected_value in data["expected_headers"].items():
            assert response.headers.get(header) == expected_value, f"Expected header {header} to be {expected_value}"

    # Validate response time for "slow_response" cases
    if "expected_delay" in data:
        assert response_time >= data["expected_delay"], f"Response time should be at least {data['expected_delay']} seconds"
    elif "response_time" in data:
        assert response_time < data["response_time"], f"Response time should be less than {data['response_time']} seconds"