from datetime import timedelta
from typing import Optional

from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from django.http import HttpRequest

import redis
import jwt

r = redis.Redis(
    host=settings.REDIS_HOST
)


class AccessError(Exception):
    def __init__(self):
        super(AccessError, self).__init__("access error")


def create_session(username: str, password: str) -> str:
    """
    Аутентифицирует польлзователя и если он является аминистратором
    (не обязательно superusr, достаточно staff) то выдает токен доступа
    для работы с API
    """
    user = authenticate(username=username, password=password)
    if not user:
        raise AccessError()
    token = jwt.encode({"username": user.username,
                        "exp": timezone.now() + timedelta(days=1)},
                       settings.SECRET_KEY,
                       algorithm="HS256")
    r.set(username, token)
    return token


def get_token_from_request(request: HttpRequest) -> Optional[str]:
    """
    Извлекает токен доступа из запроса
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return
    token = auth_header.split(" ")[1]
    return token


def auth(request: HttpRequest) -> bool:
    """
    авторизует пользователя по токену
    """
    token = get_token_from_request(request)
    if not token:
        return False
    try:
        jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms="HS256"
        )
        return True
    except jwt.exceptions.InvalidTokenError as e:
        return False



