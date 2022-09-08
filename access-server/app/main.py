import os
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKey

from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_200_OK
from starlette.responses import Response, FileResponse

from .model.user import User
from .model.instance import Instance
from .deps import *
from .db import db
from .constants import *
from .internal.instance import create_instance, stop_instance

INDEX = os.path.join(os.path.dirname(__file__), 'www', 'index.html')

def main():
    app = FastAPI()
    db.init_db()

    @app.get("/")
    def root():
        return FileResponse(INDEX)
    
    @app.get("/config")
    def GET_config():
        return {
            
        }

    @app.get("/user")
    def GET_user(user: User = Depends(get_user)):
        return user

    @app.get("/instance")
    def GET_instance(instance: Instance = Depends(get_instance)):
        return instance

    @app.put("/instance")
    def PUT_instance(user: User = Depends(get_user), instance: Instance = Depends(get_instance)):
        if instance is not None:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail="Instance exists"
            )
        print(instance)

        with db.get_db() as conn:
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
        
        return new_instance

    @app.delete("/instance")
    def DELETE_instance(instance: Instance = Depends(get_instance)):
        if instance is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Instance does not exist"
            )

        with db.get_db() as conn:
            stop_instance(instance)

            db.queries.instances.remove_by_token(conn, instance.user_token)
        
        return Response(status_code=HTTP_200_OK)

    return app