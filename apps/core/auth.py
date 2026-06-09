from functools import wraps
from django.shortcuts import redirect

AUTH_SESSION_KEY = 'auth'
USER_ROLE = 'user'
AUCTIONEER_ROLE = 'auctioneer'


def get_auth(request):
    return request.session.get(AUTH_SESSION_KEY)


def login_session(request, auth_data):
    request.session[AUTH_SESSION_KEY] = auth_data
    request.session.modified = True


def logout_session(request):
    request.session.pop(AUTH_SESSION_KEY, None)
    request.session.modified = True


def auth_required(login_url='user:login'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            auth = get_auth(request)
            if not auth:
                return redirect(login_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_role(role, login_url):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            auth = get_auth(request)
            if not auth or auth.get('role') != role:
                return redirect(login_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


user_required = require_role(USER_ROLE, 'user:login')
auctioneer_required = require_role(AUCTIONEER_ROLE, 'auctioneer:login')
