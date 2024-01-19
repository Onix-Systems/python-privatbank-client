from rest_framework import status
from rest_framework.exceptions import APIException


class PrivatDoesNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Privatbank not added."
    default_code = "Privatbank_not_added."


class PrivatExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Privatbank already added."
    default_code = "Privatbank_already_added."
