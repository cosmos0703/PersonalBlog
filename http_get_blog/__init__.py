from typing import Mapping
import logging
import json
import azure.functions as func
from ..shared.storage import BlogTable
from ..shared.security import Authenticate


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'{req.method} v1/api/blogs')
    if req.method == 'GET':
        return http_get(req)
    if req.method == 'POST':
        return http_post(req)

    return func.HttpResponse(status_code=400)

@Authenticate()
def http_get(req: func.HttpRequest) -> func.HttpResponse:
    bt = BlogTable()
    return func.HttpResponse(
        body=json.dumps(bt.list_blogs()),
        mimetype='application/json',
        status_code=200
    )

@Authenticate()
def http_post(req: func.HttpRequest) -> func.HttpResponse:
    bt = BlogTable()
    return func.HttpResponse(
        body=json.dumps(bt.list_blogs()),
        mimetype='application/json',
        status_code=200
    )
