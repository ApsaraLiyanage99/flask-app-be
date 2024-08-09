import bcrypt
import jwt
import datetime
from dataclasses import dataclass
import logging

@dataclass
class User:
    username: str
    password: str
    refresh_token: str = None

    @staticmethod
    async def create_user(db, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = """ INSERT INTO users (username, password) VALUES (%s, %s) """
        await db.execute(query, username, hashed_password)

    @staticmethod
    async def get_user_by_username(db_handler, username):
        query = "SELECT id, password FROM users WHERE username = %s"
        result = await db_handler.execute(query, username)
        return result[0] if result else None
    
    @staticmethod
    async def generate_token(user_id, secret_key, expires_in):
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.now(datetime.timezone.utc)  + datetime.timedelta(seconds=expires_in)
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    
    @staticmethod
    async def store_or_update_refresh_token(db, user_id, token, expires_in=86400):
        expiry_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)
        if expiry_date is None:
            logging.error("Refresh token expiry date couldn't be set")
            return False
        try:
            existing_token = await User.get_refresh_token_by_user_id(db, user_id)
            if existing_token:
                query = "UPDATE refresh_tokens SET token = %s, expiry_date = %s WHERE user_id = %s"
                await db.execute(query, token, expiry_date, user_id)
            else:
                query = "INSERT INTO refresh_tokens (user_id, token, expiry_date) VALUES (%s, %s, %s)"
                await db.execute(query, user_id, token, expiry_date)
            return True
        except Exception as e:
            logging.error(f"Error storing or updating refresh token: {e}")
            return False
        
    @staticmethod
    async def get_refresh_token_by_user_id(db, user_id):
        query = "SELECT token FROM refresh_tokens WHERE user_id = %s"
        result = await db.execute(query, user_id)
        return result[0] if result else None
        
    @staticmethod
    def decode_token(token, jwt_secret_key):
        try:
            payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            return None
        except Exception as e:
            logging.error(f"Error decoding token: {e}")
            return None
        
    @staticmethod
    async def delete_refresh_token(db, user_id):
        try:
            query = "DELETE FROM refresh_tokens WHERE user_id = %s"
            result = await db.execute(query, user_id)
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting refresh token: {e}")
            return False
        

    @staticmethod
    async def remove_expired_tokens(db):
        query = "DELETE FROM refresh_tokens WHERE expiry_date < %s"
        try:
            await db.execute(query, datetime.datetime.now(datetime.timezone.utc))
            logging.info("Expired tokens removed successfully.")
        except Exception as e:
            logging.error(f"Error removing expired tokens: {e}")

    @staticmethod
    async def get_name_by_userid(db, user_id):
        query = "SELECT username FROM users WHERE id = %s"
        result = await db.execute(query, user_id)
        return result[0] if result else None
