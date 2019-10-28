import logging

import azure.functions as func
from __app__.shared import config


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(f"Hello {config.ROOT_DIR}!")
