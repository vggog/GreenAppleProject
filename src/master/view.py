from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, Response, Cookie
from starlette import status

from src.core.schemas import ResponseAccessToken
from src.master.service import Servise
from src.core.authorization import Authorization
from src.master.schemas import RepairOrderSchema, CreateRepairOrderSchema


router = APIRouter(
    prefix='/master',
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='master/auth')


@router.post(
    '/auth',
    response_model=ResponseAccessToken,
)
def authorize_master(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        servise=Depends(Servise),
        authorization=Depends(Authorization),
):
    """
       Authorization of the master and issuance of an access token and refresh
       token.
       """
    response_code, detail = servise.get_master(form_data.username, form_data.password)
    if response_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response_code,
            detail=detail,
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
    "/refresh",
    response_model=ResponseAccessToken,
)
def master_refreshing(
        response: Response,
        refresh_token: Optional[str] = Cookie(None),
        authorization=Depends(Authorization),
        service=Depends(Servise)
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    data = authorization.get_data_from_jwt(refresh_token)

    if not service.get_master_by_phone(data["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

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
    "/repair_orders",
    response_model=RepairOrderSchema,
)
def create_repair_order(
        repair_order: CreateRepairOrderSchema,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Servise = Depends(Servise),
        authorization=Depends(Authorization),
):
    data_from_jwt = authorization.get_data_from_jwt(token)

    if not service.get_master_by_phone(data_from_jwt["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    created_order = service.create_repair_order(
        repair_order,
        phone_number=data_from_jwt["sub"]
    )

    return created_order
