from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Extract code from the exception detail if it exists
        error_code = (
            response.data.get("code", None) if isinstance(response.data, dict) else None
        )
        error_detail = (
            response.data.get("detail", None)
            if isinstance(response.data, dict)
            else str(response.data)
        )

        custom_response_data = {
            "status": "failed",
            "status_code": response.status_code,
            "error": {"code": error_code, "detail": error_detail},
        }
        response.data = custom_response_data

    return response


# utils/handlers.py
