from fastapi import Depends, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery

from starlette.status import HTTP_403_FORBIDDEN, HTTP_409_CONFLICT

from .constants import API_KEY_NAME

from .db.db import get_db, queries

from .model.instance import Instance
from .model.user import User

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

def check_busy(token: str = Security(api_key_query)):
    busy = queries.instances.get_busy_by_token(get_db(), token)
    busy = 0 if busy is None else busy
    if busy == 0:
        return busy
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="Resource busy"
        )

def validate_token(token: str = Security(api_key_query)):
    with get_db() as conn:
        user_dict = queries.users.get_by_token(conn, token)
        if user_dict is not None:
            return token
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )

def get_user(token: str = Depends(validate_token)):
    with get_db() as conn:
        user_dict = queries.users.get_by_token(conn, token)
        if user_dict is None:
            return None
        return User.parse_obj(user_dict)

def get_instance(token: str = Depends(validate_token)):
    with get_db() as conn:
        instance_dict = queries.instances.get_by_token(conn, token)
        if instance_dict is None:
            return None
        return Instance.parse_obj(instance_dict)