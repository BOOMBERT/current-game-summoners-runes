import requests


def get_info_from_authorized_api_request(
        api_info: str, info_to_request: str, api_key: str
) -> requests.Response:
    return requests.get(url=f"{api_info}{info_to_request}", params={"api_key": api_key})


def check_the_request_for_error(request: requests.Response) -> bool:
    try:
        request.raise_for_status()
        return True

    except requests.exceptions.RequestException as request_error:
        current_error_code = request_error.response.status_code
        error_reason = request_error.response.reason

        raise SystemExit(
            f"Error code: {current_error_code}\n"
            f"Error message: {error_reason}"
        ) from request_error
