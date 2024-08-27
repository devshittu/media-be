from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, ErrorDetail
import logging

logger = logging.getLogger('app_logger')


def custom_exception_handler(exc, context):
    logger.debug(f"Exception received: {exc}")
    logger.debug(f"Context: {context}")

    response = exception_handler(exc, context)

    if response is not None:
        logger.debug(f"Initial response data: {response.data}")

        # Handle ValidationError separately
        if isinstance(exc, ValidationError):
            detail = {}
            for field, errors in exc.detail.items():
                logger.debug(f"Field: {field}, Errors: {errors}")
                # Convert ErrorDetail to string using str()
                if isinstance(errors, list):
                    # Convert each ErrorDetail in the list to a string
                    detail[field] = " ".join([str(e) for e in errors])
                elif isinstance(errors, ErrorDetail):
                    # Convert single ErrorDetail to a string
                    detail[field] = str(errors)
                else:
                    # Handle case where errors are plain strings
                    detail[field] = errors
            error_code = "invalid_data"
            error_detail = detail
            logger.debug(f"Processed ValidationError details: {error_detail}")
        else:
            # Handle non-validation errors (which might still include ErrorDetail objects)
            error_code = response.data.get("code", "invalid_data")
            error_detail = response.data.get("detail", "")

            # Convert top-level ErrorDetail if needed
            if isinstance(error_code, ErrorDetail):
                error_code = str(error_code)
            if isinstance(error_detail, ErrorDetail):
                logger.debug(
                    f"error_detail is an instance of ErrorDetail: {str(error_detail)}")
                error_detail = str(error_detail)

            logger.debug(f"Unwrapped error code: {error_code}")
            logger.debug(f"Unwrapped error detail: {error_detail}")

        custom_response_data = {
            "status": "failed",
            "status_code": response.status_code,
            "error": {
                "code": error_code,
                "detail": error_detail,
            },
        }
        logger.debug(f"Final response data: {custom_response_data}")
        response.data = custom_response_data

    return response

# utils/handlers.py
