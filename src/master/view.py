from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, Response, Cookie
from starlette import status
from fastapi.responses import FileResponse, StreamingResponse

from src.core.schemas import ResponseAccessToken
from src.master.service import Servise
from src.core.authorization import Authorization
from src.master.schemas import (
    RepairOrderSchema, CreateRepairOrderSchema, AllInfoOfRepairOrderSchema,
    UpdatedRepairOrderSchema, QuickInfoRepairOrderSchema
)


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


@router.get(
    "/repair_orders/all",
    response_model=list[QuickInfoRepairOrderSchema],
)
def get_all_repair_orders(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Servise = Depends(Servise),
        authorization=Depends(Authorization),
):
    data_from_jwt = authorization.get_data_from_jwt(token)

    if not service.get_master_by_phone(data_from_jwt["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    repair_orders = service.get_all_repair_orders()

    return repair_orders


@router.get(
    "/repair_orders/{repair_order_id}",
    response_model=AllInfoOfRepairOrderSchema,
)
def get_repair_order_info(
        repair_order_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Servise = Depends(Servise),
        authorization=Depends(Authorization),
):
    data_from_jwt = authorization.get_data_from_jwt(token)

    if service.get_master_by_phone(data_from_jwt["sub"]) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    repair_order = service.get_repair_order(repair_order_id)

    if repair_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return repair_order


@router.patch(
    "/repair_orders/{repair_order_id}",
    response_model=AllInfoOfRepairOrderSchema,
)
def update_repair_order(
        repair_order_id: int,
        updated_repair_order: UpdatedRepairOrderSchema,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Servise = Depends(Servise),
        authorization=Depends(Authorization),
):
    data_from_jwt = authorization.get_data_from_jwt(token)

    if service.get_master_by_phone(data_from_jwt["sub"]) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    status_code, repair_order = service.update_repair_order_info(
        repair_order_id, updated_repair_order
    )

    if status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code,
            detail=repair_order,
        )

    return repair_order


@router.get(
    "/repair_orders/receipt/{repair_order_id}",
)
def get_receipt_of_repair_order(
        repair_order_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Servise = Depends(Servise),
        authorization=Depends(Authorization),
):
    data_from_jwt = authorization.get_data_from_jwt(token)

    if service.get_master_by_phone(data_from_jwt["sub"]) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    status_code, detail = service.generate_receipt(
        repair_order_id
    )

    if status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code,
            detail=detail,
        )

    return Response(
        content=detail,
        headers={
            "Content-Disposition": 'inline; filename="out.pdf"',
            "content-type": "application/octet-stream",
            "Content-Transfer-Encoding": "binary"
        }
    )
