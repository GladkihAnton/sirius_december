import json
from typing import Callable

from fastapi import Request, Response, exceptions
from fastapi.routing import APIRoute
from loguru import logger


class LogRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            logger.info(f"{request.method} {request.url}")
            params_items = request.path_params.items()
            if params_items:
                logger.info(f"Params: {params_items}")

            headers_dict = dict(request.headers)
            if 'authorization' in headers_dict:
                headers_dict['authorization'] = 'hidden'

            logger.info(f"Headers: {headers_dict.items()}")

            body = await request.body()
            if isinstance(body, bytes):
                text_string = body.decode('utf-8')
                filename_start = text_string.split('filename="')[-1]
                filename = filename_start.split('"')[0]
                logger.info(f"filename: {filename}")
            else :
                logger.info(f"request body: {json.loads(body)}")

            try:
                response: Response = await original_route_handler(request)
            except exceptions.HTTPException as e:
                logger.error(f'{e.status_code}, {e.detail}')
                raise e
            except exceptions.RequestValidationError as e:
                # логируем ошибки валидации в удобном виде (используя __str__)
                logger.error(e)
                raise e
            except Exception as e:
                logger.exception(e)
                raise e

            logger.info(f"route response status_code={response.status_code}")
            if hasattr(response, 'body'):
                body = json.loads(response.body)
                if body and 'result' in body:
                    res = {i: k for i, k in body.items() if 'result' not in i}
                else:
                    res = body
                logger.info(f"route response body={res}")
            return response

        return custom_route_handler
