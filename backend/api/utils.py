from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        'Http404': handle_generic_error,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response
    # if response is not None:
    #     response.data['status_code'] = response.status_code

    # return response#


def handle_generic_error(exc, context, response):
    response.data['detail'] = 'Страница не найдена.'
    return response
