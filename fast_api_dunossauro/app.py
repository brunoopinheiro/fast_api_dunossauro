from fastapi import FastAPI
from fast_api_dunossauro.schemas import Message
from http import HTTPStatus

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}
