from rest_framework.exceptions import APIException
from rest_framework import status 

class CustomBadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A bad request occurred.'
    default_code = 'bad_request'


# from dj43_project.exceptions import CustomBadRequest

# def some_view(request):
#     ...
#     if some_error_condition:
#         raise CustomBadRequest(detail="Specific error message here.")
#     ...