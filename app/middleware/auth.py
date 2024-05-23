from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from typing import List
import time
from app.auth.authenticate import userfromauthenticate
from app.models.request_log import RequestLog

EXCLUDE_PATHS = [
    "/css", "/images", "/js", "/favicon.ico", "/errors", '/users/form',
    '/mains/list', '/devtemplates/list', '/teams/list',
    "/comodules/main", "/comodules/list", '/comodules/v1', '/comodules/r',
    "/communities/list", '/communities/r', '/securities', '/boards'
]

ROLE_BASED_ACCESS = {
    "GUEST": ["/comodules", '/users/read', '/communities'],
    "PARTNER": ["/devtemplates", "/teams"],
    "ADMIN": ["/admins", '/commoncodes', '/users']
}

async def auth_middleware(request: Request, call_next):
    user = await userfromauthenticate(request)
    request.state.user = user

    if not (any(request.url.path.startswith(path) for path in EXCLUDE_PATHS) or request.url.path == '/'):
        user_roles: List[str] = user.get("roles", [])
        path_allowed = False
        for role in user_roles:
            if any(request.url.path.startswith(path) for path in ROLE_BASED_ACCESS.get(role, [])):
                path_allowed = True
                break

        if not path_allowed:
            return RedirectResponse(url="/securities/login_google")

    response = await call_next(request)
    await log_request_response(request, response, user)
    return response

async def log_request_response(request: Request, response: Response, user):
    start_time = time.time()
    parameters = {}
    if request.method == "GET":
        parameters = dict(request.query_params)
    end_time = time.time()
    duration = end_time - start_time

    log_data = RequestLog(
        request={
            "method": request.method,
            'header': dict(request.headers),
            "parameters": parameters,
        },
        response={
            "status_code": response.status_code,
        },
        duration=duration,
        user=user
    )

    await log_data.insert()
