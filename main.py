from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from validators import check_incoming_data, incoming_parser, find_form, return_right_type

app = FastAPI()


@app.post("/get_form")
async def root(request: Request):  # incoming: str | request: Request
    incoming = str(request.query_params)
    incoming_dict = await incoming_parser(incoming)
    if not incoming_dict:
        return {'message': 'Входные данные не соответствуют заявленному шаблону'}
    found_form = await find_form(incoming_dict)
    if found_form:
        result = await check_incoming_data(found_form, incoming_dict)
        if result:
            return result

    response = await return_right_type(incoming_dict)
    return JSONResponse(content=response, status_code=400)

@app.get("/get_form")
async def get_response():
    return {'message': 'Сервер принимает только POST запросы'}
