from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail, status


def replace_error_detail(response, status, code, new_message):
    if response.status_code == status and response.data["detail"].code == code:
        response.data["detail"] = ErrorDetail(new_message, code)

    return response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response = replace_error_detail(
            response,
            status.HTTP_401_UNAUTHORIZED,
            "not_authenticated",
            "Token autentikasi tidak diberikan.",
        )
        response = replace_error_detail(
            response,
            status.HTTP_401_UNAUTHORIZED,
            "authentication_failed",
            "Salah token.",
        )

    return response
