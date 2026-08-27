from functools import wraps

def require_role(role):
    def decorator(function):
        @wraps(function)
        def wrapper(user, *args, **kwargs):
            if role not in user.roles:
                raise PermissionError(f"missing role: {role}")
            return function(user, *args, **kwargs)
        return wrapper
    return decorator
