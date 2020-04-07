from fastapi import FastAPI
import psycopg2
import sys
import pytz
from datetime import datetime

#All constants declaration
tz = pytz.timezone('Asia/Shanghai')
BJ_Time = datetime.now(tz)
site_url = "http://site.com"
site_domain_mane = "site.com"



#start the main apai loop
app = FastAPI()

@app.get("/suatus")#this is for heartbeat to detect the client status
async def status_check(user_id: int, time_stamp: int ,status: bool):#接收状态信息
    return("status" , "OK")

@app.get("/ping")#this is for getting the ping of the server 
async def root():
    return("status" , "OK")

@app.get("/login/")
async def read_item(username: int, password: str, time: int): #这里是登录API,主要实现功能是客户端点击login将get http://site.com/login/?username=2&password=2&time=200303031211
    user_information = {"username": username,"password": password,"time":time}
    return user_information

