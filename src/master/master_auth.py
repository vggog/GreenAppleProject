from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette import status

from src.core.authorization import Authorization
from src.master.service import Servise


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='master/auth')


def get_master(
        token: Annotated[str, Depends(oauth2_scheme)],
        authorization=Depends(Authorization),
        service=Depends(Servise),
):
    data_from_jwt = authorization.get_data_from_jwt(token)
    master = service.get_master_by_phone(data_from_jwt["sub"])

    if not master:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return master
