from fastapi import FastAPI
import base64
from Crypto.Cipher import AES
import psycopg2
import sys
import string
import pytz
from datetime import datetime
import site_settings
import random
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from fastapi.middleware.cors import CORSMiddleware


#All constants declaration
tz = pytz.timezone('Asia/Shanghai')
BJ_Time = datetime.now(tz)
site_url = site_settings.site_url
api_url = site_settings.api_url
aes_key = site_settings.aes_key
html = site_settings.html
hash_hey = site_settings.hash_key

#program startups
app = FastAPI()
conn = psycopg2.connect(database="TEST1", user="postgres", password="dachengzi", host="10.0.10.102", port="5432") #password in this line is invalid 
cur = conn.cursor()

#接入CORS
origins = [
    "http://localhost",
    "http://localhost:6000",
    "http://dev.sunboy.site",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*:"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
async def read_item(username: str , password: str, time: str): #这里是登录API,主要实现功能是客户端点击login将get http://site.com/login/?username=2&password=2&time=200303031211
    user_information = {"username": username,"password": password,"time":str}
    #进入登录验证部分
    real_pass = get_real_pass(password,time)
    init = "ACCOUNT = '" + username + "'"
    result = SELECT_FUNC('USERS',init)
    print(result)
    if check_password_hash(result[5],real_pass):
        if result[7]=='ADMIN':
            login_admin_item = {"status" : "OK",
            "redirect_url" : site_url + '/Admin',
            "user_id" : result[0],
            "token" : token_create(),
            "AUTH" : str.upper(result[7]),
            "tab" : 0
            }
            print(login_admin_item)
            return login_admin_item
        elif result[7]=='STUDENT':
            login_stu_item = {"status" : "OK",
            "redirect_url" : site_url + '/MainPage',
            "user_id" : result[0],
            "token" : token_create(),
            "AUTH" : str.upper(result[7]),
            "tab" : 0
            }
            print(login_stu_item)
            return login_stu_item
        elif result[7]=='TEACHER':
            login_teacher_item = {"status" : "OK",
            "redirect_url" : site_url + '/Teacher',
            "user_id" : result[0],
            "token" : token_create(),
            "AUTH" : str.upper(result[7]),
            "tab" : 0
            }
            print(login_admin_item)
            return login_admin_item
        else:
            pass

    else:
        return "AUTH_ERROR"







##获取前端弱鸡加密过的密码
def get_real_pass(password,time):
    encoder = base64.b64decode(password.encode('utf-8'))
    decode_string = encoder.decode('utf-8')
    i = len(decode_string)
    if int(time) < 10 :
        real_pass = decode_string[1:i-1]
    else :
        real_pass = decode_string[2:i-2]
    return str(real_pass)

##插库驱动函数（单字段
def INSERT_FUNC(table,*args):
    pass

##查库驱动函数（单字段 单条件 单返回结果
def SELECT_FUNC(table,operators):
    sql = "SELECT * FROM " + table + " WHERE " + operators
    cur.execute(sql)
    return cur.fetchone()

#创建一个token 并初始化信息
def token_create(user_id,time):
    OUT_FLAG = False
    MAIN_LOOP_COUNTER = 0
    TOKEN_STRING = ''#不知道这么写会不会翻车
    while True:
        if OUT_FLAG:
            TOKEN_MIDDLE_STRING = user_id[MAIN_LOOP_COUNTER] + time[MAIN_LOOP_COUNTER]#这句拼接之
            TOKEN_STRING = TOKEN_STRING + TOKEN_MIDDLE_STRING#把局部变量搬到外部变量
            MAIN_LOOP_COUNTER = MAIN_LOOP_COUNTER + 1#把counter加1
            if user_id.len() - 1 == MAIN_LOOP_COUNTER:#这是判断任意字符串是否达到了他的最高长度，在处理时间时，已将其增加为16位长度字符串。所以就默认userid短了。
                OUT_FLAG = True#如果达到了就跳转到另一个分支
            else :
                pass
        else :
            TOKEN_STRING = TOKEN_STRING + time[MAIN_LOOP_COUNTER,time.len()-MAIN_LOOP_COUNTER]
            break
    
    return "9b21a27b5cc"


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

