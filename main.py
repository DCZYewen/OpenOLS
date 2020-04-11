from fastapi import FastAPI
import base64
from Crypto.Cipher import AES
import psycopg2
import sys
import pytz
from datetime import datetime
import site_settings

#All constants declaration
tz = pytz.timezone('Asia/Shanghai')
BJ_Time = datetime.now(tz)
site_url = "http://site.com"
site_domain_mane = "site.com"
aes_key = site_settings.aes_key
html = site_settings.html

#start the main apai loop
app = FastAPI()

@app.get("/")#This is for main page
async def root():
    return(html)

@app.get("/status")#this is for heartbeat to detect the client status
async def status_check(user_id: int, time_stamp: int ,status: bool):#接收状态信息
    return("status" , "OK")

@app.get("/ping")#this is for getting the ping of the server 
async def root():
    return("status" , "OK")

@app.get("/login/")
async def read_item(username: int, password: str, time: int): #这里是登录API,主要实现功能是客户端点击login将get http://site.com/login/?username=2&password=2&time=200303031211
    user_information = {"username": username,"password": password,"time":time}
    return user_information
    #进入登录验证部分
    real_pass = get_real_pass(password,time)
    encrypted_pass = encrypt_oracle(aes_key,real_pass)







##This for encryption and so on .
def get_real_pass(password,time):
    decode_string = base64.b64decode(password)
    i = len(decode_string)
    if time < 10 :
        real_pass = decode_string[1:i-1]
    else :
        real_pass = decode_string[2:i-2]
    return real_pass




#This is for AES password encryption and decryption
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

def encrypt_oracle(key,password):
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(password))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text

def decrypt_oralce(key,encrypted_text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(encrypted_text.encode(encoding='utf-8'))
    #执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','') 
    return(decrypted_text)

