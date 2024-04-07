from passlib.context import CryptContext  # Use a secure hashing library
from datetime import datetime, timedelta
import jwt

# Secret key for JWT signing (replace with a secure key)
SECRET_KEY = "263776471033"  # Move to environment variable

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password):
    """
    Hashes a plain text password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain text password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def generate_auth_token(phone_number):
    """
    Generates a JWT token containing the user's phone number as a claim.
    """
    payload = {
        "phone_number": phone_number,
        "exp": datetime.utcnow() + timedelta(minutes=60),  # Token expires in 60 minutes
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_auth_token(auth_token):
    """
    Decodes a JWT token and returns the user information (phone number).
    Raises an exception if the token is invalid.
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        return payload["phone_number"]
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

