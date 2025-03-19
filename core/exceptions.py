from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    data = response.data
    if not isinstance(data, dict):
        return response

    errors = data.pop("error", [])

    if "detail" in data:
        errors.append(data.pop("detail"))
    if "errors" in data:
        errors.extend(data.pop("errors"))

    response.data = {"errors": errors, "field_errors": data}
    return response
