import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('start')

    if req.method == 'POST':
        req_body = req.get_json()
        logging.info(req_body)

        logging.info(req_body.get('url').split('id=')[1])
        return func.HttpResponse(req_body.get('url').split('id=')[1])

    else:
        logging.warning('not arrowed method. ' + req.method)
        return func.HttpResponse('not arrowed method. ' + req.method, status_code=403)
