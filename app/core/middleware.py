from functools import wraps
from flask import request, g
import app.core.const as const
import jwt
import os
import logging

def authenticator():
    """
    Middleware to handle JWT token validation and extract user information.
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                try:
                    payload = jwt.decode(token, const.JWT_SECRET_KEY, algorithms=["HS256"])
                    g.current_user_id = payload['user_id']
                    return await f(*args, **kwargs)
                except jwt.ExpiredSignatureError:
                    return {"error": "Expired token"}, 401
                except jwt.InvalidTokenError:
                    return {"error": "Invalid token"}, 401
                except Exception as e:
                    logging.error(f"Error decoding token: {e}")
                    return {"error": "Internal Server Error"}, 500
            else:
                return {"error": "Token is missing"}, 401
        return decorated_function
    return decorator
