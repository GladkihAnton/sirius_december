from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException, status

from webapp.models.exceptions import DomainError, ItemNotFound


def handle_domain_error(func: Callable[[Any], Any]) -> Any:
    @wraps(func)
    async def wrapper(*args: tuple[Any], **kwargs: dict[Any, Any]) -> Callable[[Any], Any]:
        try:
            return await func(*args, **kwargs)
        except ItemNotFound as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            )
        except DomainError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            )

    return wrapper
