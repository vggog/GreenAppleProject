from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from src.core.schemas import (
    ResponseAccessToken
)
from src.admin.service import Service
from src.core.authorization import Authorization
from src.admin.schemas import (
    MasterInfoWithPassword, MasterInfoWithIdSchema, MasterUpdateSchema,
    MasterInfoSchema
)


router = APIRouter(
    prefix="/admin",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/auth")


@router.post(
    "/auth",
    response_model=ResponseAccessToken,
)
def authorize_admin(
        response: Response,
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

    response.set_cookie(
        "refresh_token",
        value=refresh_token,
        httponly=True
    )

    return ResponseAccessToken(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/auth/refresh",
    response_model=ResponseAccessToken,
)
def authorize_admin(
        response: Response,
        refresh_token: Optional[str] = Cookie(None),
        authorization=Depends(Authorization),
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    data = authorization.get_data_from_jwt(refresh_token)

    access_token = authorization.create_access_token(
        data={"sub": data["sub"]}
    )
    refresh_token = authorization.create_refresh_token(
        data={"sub": data["sub"]}
    )

    response.set_cookie(
        "refresh_token",
        value=refresh_token,
        httponly=True
    )

    return ResponseAccessToken(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/logout",
)
def admin_logout(
        response: Response,
):
    response.delete_cookie("refresh_token")
    return {"status": "success"}


@router.post(
    "/master",
    response_model=MasterInfoWithPassword,
)
def add_new_master(
        master: MasterInfoWithPassword,
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


@router.get(
    "/master/all",
    response_model=list[MasterInfoWithIdSchema],
)
def get_all_masters(
        token: Annotated[str, Depends(oauth2_scheme)],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    """
    Выдаёт всех мастеров, которые есть в базе данных.
    """
    username = authorization.get_data_from_jwt(token)["sub"]

    if not service.is_admin(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return service.get_all_masters()


@router.get(
    "/master/{master_id}",
    response_model=MasterInfoWithIdSchema,
)
def get_master_info(
        master_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    """
    Выдаёт информацию о конкретном мастере.
    """
    username = authorization.get_data_from_jwt(token)["sub"]

    if not service.is_admin(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    master = service.get_master(master_id)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return master


@router.put(
    "/master/{master_id}",
    response_model=MasterInfoSchema,
)
def update_master_info(
        master_id: int,
        master_info: MasterUpdateSchema,
        token: Annotated[str, Depends(oauth2_scheme)],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    """
    Обновление данных у мастера.
    """
    username = authorization.get_data_from_jwt(token)["sub"]

    if not service.is_admin(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    status_code, response = service.update_master(master_id, master_info)
    if status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_code,
            detail=response,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@router.delete(
    "/master/{master_id}",
    response_model=MasterInfoSchema,
)
def delete_master_info(
        master_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    """
    Удаление мастера.
    """
    username = authorization.get_data_from_jwt(token)["sub"]

    if not service.is_admin(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    status_code, response = service.delete_master(master_id)

    if status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_code,
            detail=response,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response
