from fastapi import FastAPI


app = FastAPI()

#The officail sample of FastAPI

@app.get("/suatus")#this is for heartbeat to detect the client status
def status_check(user_id: int, time_stamp: int ,status: bool):#接收状态信息
    return("status" , "OK")

@app.get("/ping")#this is for getting the ping of the server 
def root():
    return("status" , "OK")

@app.get("/login/")
def read_item(username: int, password: str, time_stamp: int): #这里是登录API,主要实现功能是客户端点击login将get http://site.com/login/?username=2&password=2&time=200303031211
    user_information = {"username": username,"password": password,"time_stamp":time_stamp}
    return user_information



