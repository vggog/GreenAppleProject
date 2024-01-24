from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.admin.service import Service
from src.core.authorization import Authorization


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/auth")


def is_admin(
        token: Annotated[str, Depends(oauth2_scheme)],
        authorization=Depends(Authorization),
        service=Depends(Service),
):
    username = authorization.get_data_from_jwt(token)["sub"]

    if not service.is_admin(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission.",
            headers={"WWW-Authenticate": "Bearer"},
        )
