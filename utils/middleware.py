import logging


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        # self.logger = logging.getLogger(__name__)
        self.logger = logging.getLogger("global")

    def __call__(self, request):
        # Log request headers
        self.logger.info(f"Request Headers: {request.headers}")

        response = self.get_response(request)

        # Log response headers
        self.logger.info(f"Response Headers: {response.headers}")

        return response


# utils/middleware.py
