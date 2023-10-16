from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from src.core.schemas import (
    ResponseTokens, ResponseAccessToken, RequestRefreshToken
)
from src.admin.service import Service
from src.core.authorization import Authorization
from src.admin.schemas import MasterInfoSchema


router = APIRouter(
    prefix="/admin",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/auth")


@router.post(
    "/auth",
    response_model=ResponseTokens,
)
def authorize_admin(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    """
    Authorization of the admin and issuance of an access token and refresh
    token.
    """
    is_valid = service.is_valid_admin_conf(
        form_data.username,
        form_data.password
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = authorization.create_access_token(
        data={"sub": form_data.username}
    )
    refresh_token = authorization.create_refresh_token(
        data={"sub": form_data.username}
    )

    return ResponseTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/auth/refresh",
    response_model=ResponseAccessToken,
)
def authorize_admin(
        token: RequestRefreshToken,
        authorization=Depends(Authorization),
):
    data = authorization.get_data_from_jwt(token.refresh_token)

    access_token = authorization.create_access_token(
        data={"sub": data["sub"]}
    )

    return ResponseAccessToken(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/master",
    response_model=MasterInfoSchema,
)
def add_new_master(
        master: MasterInfoSchema,
        token: Annotated[str, Depends(oauth2_scheme)],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    username = authorization.get_data_from_jwt(token)["sub"]

    if not service.is_admin(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    success, detail = service.add_master(master)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return master
