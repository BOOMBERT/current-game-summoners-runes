import requests


def get_info_from_request(api_info: str, info_to_request: str, api_key: str) -> requests.Response:
    return requests.get(url=f"{api_info}{info_to_request}", params={"api_key": api_key})


def check_the_request_for_error(request: requests.Response, error_message: str) -> bool:
    try:
        request.raise_for_status()

        return True

    except requests.exceptions.RequestException as request_error:
        NO_ACCESS_CODE = 404
        current_error_code = request_error.response.status_code

        if current_error_code == NO_ACCESS_CODE:
            print(error_message)

        else:
            print(
                f"Error code: {current_error_code}\n"
                f"Error message: {request_error.response.reason}"
            )

    return False
