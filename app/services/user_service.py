from app.models.user_model import User
import bcrypt
import app.core.const as const
import logging
from flask import g

class UserService:
    @staticmethod
    async def register_user(data, db_handler):
        username = data.get('username')
        password = data.get('password')

        if username == password:
            return {"error": "Username and password cannot be the same"}, 400

        if not password.isalnum():
            return {"error": "Password must be alphanumeric"}, 400
    
        try:
            user = await User.get_user_by_username(db_handler, username)
            if user:
                return {"error": "User already exists"}, 400

            success = await User.create_user(db_handler, username, password)

            return {"message": "User registered successfully"}, 201
        except Exception as e:
            return {"error": f"Error registering user: {e}"}, 500

    @staticmethod
    async def login_user(data, db_handler):
        try:
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {"error": "Missing username or password"}, 400

            user = await User.get_user_by_username(db_handler, username)
            if user is None:
                return {"error": "User does not exist"}, 401

            user_id, hashed_password = user

            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return {"error": "Password mismatched"}, 401
            
            access_token = await User.generate_token(user_id, const.JWT_SECRET_KEY, 3600)
            refresh_token = await User.generate_token(user_id, const.JWT_SECRET_KEY, 86400)

            success = await User.store_or_update_refresh_token(db_handler, user_id, refresh_token, 86400)
            if not success:
                logging.error("Refresh token couldn't be stored")
                return {"error": "Refresh token couldn't be stored"}, 500

            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        except Exception as e:
            logging.error(f"Error logging in user: {e}")
            return {"error": "Internal Server Error"}, 500
    
    @staticmethod
    async def refresh_token(refresh_token, db_handler):
        try:
            payload = User.decode_token(refresh_token, const.JWT_SECRET_KEY)
            if payload is None:
                return {"error": "Invalid or expired refresh token"}, 401

            new_access_token = User.generate_token(payload['user_id'], const.JWT_SECRET_KEY, 3600)
            new_refresh_token = User.generate_token(payload['user_id'], const.JWT_SECRET_KEY, 86400)
            if not new_access_token or not new_refresh_token:
                return {"error": "Error generating new tokens"}, 500
                
            success = await User.store_or_update_refresh_token(db_handler, payload['user_id'], new_refresh_token, 86400)
            if not success:
                return {"error": "Refresh token couldn't be stored"}, 500

            return {"access_token": new_access_token, "refresh_token": new_refresh_token}, 200

        except Exception as e:
            logging.error(f"Error refreshing token: {e}")
            return {"error": "Internal Server Error"}, 500

    @staticmethod
    async def logout(refresh_token, db_handler):
        try:
            success = await User.delete_refresh_token(db_handler, g.current_user_id)
            if not success:
                return {"error": "Error logging out user"}, 500

            return {"message": "User logged out successfully"}, 200

        except Exception as e:
            logging.error(f"Error logging out user: {e}")
            return {"error": "Internal Server Error"}, 500
