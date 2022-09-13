import os
import uuid
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKey

from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_200_OK
from starlette.responses import Response, FileResponse

from .model.user import User, UserRequest
from .model.instance import Instance
from .deps import *
from .db import db
from .constants import *
from .internal.instance import create_instance, stop_instance

INDEX = os.path.join(os.path.dirname(__file__), 'www', 'index.html')

def periodic():
    with db.get_db() as conn:
        for inst in db.queries.instances.get_all(conn):
            instance = Instance.parse_obj(inst)
            if datetime.now(instance.end_date.tzinfo) >= instance.end_date:
                db.queries.instances.change_busy(conn, busy=1, user_token=instance.user_token)
                stop_instance(instance)
                db.queries.instances.remove_by_token(conn, instance.user_token)

def main():
    app = FastAPI()
    db.init_db()

    @app.get("/")
    def root():
        return FileResponse(INDEX)
    
    @app.get("/config")
    def GET_config():
        return CONFIG

    @app.get("/user")
    def GET_user(user: User = Depends(get_user)):
        return user

    @app.put("/user")
    def PUT_user(user_request: UserRequest):
        name = user_request.name
        token = uuid.uuid4().hex

        with db.get_db() as conn:
            db.queries.users.insert(conn, name=name, token=token)
            return token

    @app.get("/instance")
    def GET_instance(instance: Instance = Depends(get_instance)):
        return instance

    @app.put("/instance")
    def PUT_instance(user: User = Depends(get_user), instance: Instance = Depends(get_instance), busy: int = Depends(check_busy)):
        if instance is not None:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail="Instance exists"
            )
        print(instance)

        with db.get_db() as conn:
            try:
                print('set busy')
                db.queries.instances.change_busy(conn, busy=1, user_token=user.token)
                idlist = [ int(x['id']) for x in db.queries.instances.get_all_ids(conn)]
                free = list(set(range(0, MAX_ID)) - set(idlist))
                
                if len(free) <= 0:
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST, detail="Maximum number of instances, try again later"
                    )
                
                print(free[0])
                
                new_instance = create_instance(id=free[0], start_date=datetime.now(), user_token=user.token)
                if new_instance is None:
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST, detail="Can't create new instance (err code 56951411)"
                    )
                count = db.queries.instances.insert(
                    conn, **((new_instance.dict)())
                )

                print(count)
            except Exception as e:
                raise e
            finally:
                print('UNset busy')
                db.queries.instances.change_busy(conn, busy=0, user_token=user.token)
        
        return new_instance

    @app.delete("/instance")
    def DELETE_instance(instance: Instance = Depends(get_instance), busy: bool = Depends(check_busy)):
        if instance is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Instance does not exist"
            )

        with db.get_db() as conn:
            try:
                db.queries.instances.change_busy(conn, busy=1, user_token=instance.user_token)
                stop_instance(instance)
                db.queries.instances.remove_by_token(conn, instance.user_token)
            except Exception as e:
                raise e
            finally:
                db.queries.instances.change_busy(conn, busy=0, user_token=instance.user_token)
        
        return Response(status_code=HTTP_200_OK)

    return app