from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_api_dunossauro.models import User
from fast_api_dunossauro.schemas import (
    Token,
)
from fast_api_dunossauro.security import (
    create_access_token,
    verify_password,
)
from fast_api_dunossauro.types import (
    T_OAuth2Form,
    T_Session,
)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
):
    user = session.scalar(
        select(User).where(User.email == form_data.username),
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(
        data={'sub': user.email},
    )

    return {'access_token': access_token, 'token_type': 'Bearer'}
