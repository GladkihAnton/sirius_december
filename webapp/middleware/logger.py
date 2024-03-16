import uuid

from starlette.types import ASGIApp, Receive, Scope, Send

from webapp.logger import correlation_id_ctx


class LogServerMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] not in ('http', 'websocket'):
            await self.app(scope, receive, send)
            return

        for header, value in scope["headers"]:
            if header == b'x-correlation-id':
                correlation_id_ctx.set(value.decode())
                break
        else:
            correlation_id_ctx.set(uuid.uuid4().hex)

        await self.app(scope, receive, send)
