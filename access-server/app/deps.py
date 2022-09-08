from fastapi import Depends, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery

from starlette.status import HTTP_403_FORBIDDEN

from .constants import API_KEY_NAME

from .db.db import get_db, queries

from .model.instance import Instance
from .model.user import User

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

def validate_token(token: str = Security(api_key_query)):
    user_dict = queries.users.get_by_token(get_db(), token)
    if user_dict is not None:
        return token
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

def get_user(token: str = Depends(validate_token)):
    user_dict = queries.users.get_by_token(get_db(), token)
    if user_dict is None:
        return None
    return User.parse_obj(user_dict)

def get_instance(token: str = Depends(validate_token)):
    instance_dict = queries.instances.get_by_token(get_db(), token)
    if instance_dict is None:
        return None
    return Instance.parse_obj(instance_dict)