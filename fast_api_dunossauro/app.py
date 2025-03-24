from http import HTTPStatus

from fastapi import FastAPI

from fast_api_dunossauro.routers import (
    auth,
    users,
)
from fast_api_dunossauro.schemas import (
    Message,
)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}
