import azure.functions as func

def Authenticate():
    def authenticate_decorator(function):
        def func_wrapper(*args, **kwargs):
            req = getReqFromArgs(*args)
            if req is None:
                req = getReqFromKwargs(**kwargs)
            if req is None:
                return func.HttpResponse(
                    status_code=401,
                    body="Fail to decorate with Authenticate since method does not have func.request"
                )

            authorize_value = req.headers.get('Authorize')
            if authorize_value is None:
                return func.HttpResponse(
                    status_code=401,
                    body="The request does not have Authorize header"
                )
            if validateBasicAuth(authorize_value) is False:
                return func.HttpResponse(
                    status_code=401,
                    body="Failed to validate user from basic auth"
                )

            return function(*args, **kwargs)
        return func_wrapper
    return authenticate_decorator


def getReqFromArgs(*args) -> func.HttpRequest:
    for arg in args:
        if isinstance(arg, func.HttpRequest):
            return arg
    return None

def getReqFromKwargs(**kwargs) -> func.HttpRequest:
    for arg in kwargs.values():
        if isinstance(arg, func.HttpRequest):
            return arg
    return None

def validateBasicAuth(authorize_value: str) -> bool:
    # TODO: Implement Basic Auth Validation
    authorize_value = authorize_value.strip()
    basic_auth = authorize_value.strip("Basic ")
    return basic_auth
