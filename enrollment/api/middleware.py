from json import dumps
from typing import Optional, Dict, Union
from http import HTTPStatus

from aiohttp.web import middleware, Request, Response
from aiohttp.web_exceptions import HTTPException, HTTPBadRequest, HTTPInternalServerError

from marshmallow import ValidationError

def format_exception(exception: HTTPException, message: Optional[str]=None) -> HTTPException:
    exception.content_type = 'application/json'
    exception.body = dumps({
        "code": exception.status_code or 500,
        "message": message or HTTPStatus(exception.status_code).description
    })
    return exception

def format_validation_exception_message(messages_dict: Dict[Union[int, str], any]) -> str:
    queue = [messages_dict]
    messages = []
    while queue:
        item = queue.pop(0)
        if isinstance(item, dict):
            item = list(item.values())
        if isinstance(item, list):
            queue.extend(item)
        else:
            messages.append(str(item))
    return ';'.join(messages)

@middleware
async def errors_format_middleware(request: Request, handler) -> Response:
    try:
        return await handler(request)
    except HTTPException as err:
        raise format_exception(err, err.text)
    except ValidationError as err:
        raise format_exception(HTTPBadRequest(), format_validation_exception_message(err.messages))
    except Exception as err:
        raise format_exception(HTTPInternalServerError())