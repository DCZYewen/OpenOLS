from pydantic import BaseModel
##declare some models
class requestsItemPublish(BaseModel):
    action: str
    client_id: int
    ip: str
    vhost: str
    app: str
    stream: str

class requestsItemConnect(BaseModel):
    action : str
    client_id: int
    ip: str
    vhost: str
    app : str
    tcUrl : str
    pageUrl: str

class requestsItemClose(BaseModel):
    action: str
    client_id: int
    ip: str
    vhost: str
    app: str
    send_bytes: int 
    recv_bytes: int

class requestsItemUnpublish(BaseModel):
    action: str
    client_id: int
    ip: str
    vhost: str
    app: str
    stream: str

class requestsItemStop(BaseModel):
    action: str
    client_id: int
    ip: str
    vhost: str
    app: str
    stream: str

class requestsItemPlay(BaseModel):
    action: str
    client_id: int
    ip: str
    vhost: str
    app: str
    stream: str
    pageUrl: str
    param: str

class requestsItemDvr(BaseModel):
    action: str
    client_id: int
    ip: str
    vhost: str
    app: str
    stream: str
    cwd : str
    file: str