from datetime import datetime, timezone, timedelta

import bcrypt
import jwt

from src.config import auth_jwt


def encode_jwt(payload: dict,
               private_key: str = auth_jwt.private_key_path.read_text(),
               algorithm: str = auth_jwt.algorithm,
               expire_minutes: int = auth_jwt.access_token_expire_minutes) -> str:
    to_encode = payload.copy()
    to_encode['exp'] = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    encoded = jwt.encode(to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str | bytes,
               public_key: str = auth_jwt.public_key_path.read_text(),
               algorithm: str = auth_jwt.algorithm):
    decoded = jwt.decode(token, key=public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
    return hashed_password.decode()


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

