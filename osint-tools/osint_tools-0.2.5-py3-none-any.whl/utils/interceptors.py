from typing import Callable
from fastapi.routing import APIRoute
from fastapi import Request, Response
from time import time
from ..logs import logger
import datetime

class RouteTimer(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            before = time()
            response: Response = await original_route_handler(request)
            duration = time() - before
            logger.info('Route Timer: {0}'.format(duration))
            # logger.info(f"Route Headers: {response.headers}")
            return response
        return custom_route_handler


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:            
            before = time()
            response: Response = await original_route_handler(request)
            duration = time() - before

            logger.info(f"route response: {request.url} -> {duration}")
            return response

        return custom_route_handler


# @app.middleware("http")
# async def middleware_log(request: Request, call_next):
#     start_time = datetime.now()
#     method_name = request.method
#     # q_param = request.query_params
#     # p_param = request.path_params
#     content = f'''{method_name}: {request.url}'''
#     logger.info(content)
#     response = await call_next(request)
#     process_time = datetime.now() - start_time

#     response.headers["X-Time-Elapsed"] = str(process_time)
#     return response
