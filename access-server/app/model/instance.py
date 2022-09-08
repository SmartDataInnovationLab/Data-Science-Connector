from datetime import datetime
from pydantic import BaseModel

class Instance(BaseModel):
    id: int | None = None
    path: str
    start_date: datetime
    end_date: datetime
    user_token: str
    ssh_user: str
    ssh_pass: str
    ssh_port: str
    