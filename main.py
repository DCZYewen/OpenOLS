from fastapi import FastAPI , Response
from starlette.requests import Request
import base64
import hashlib
import psycopg2
import sys,string,requests,time,random
import Lib.site_settings as site_settings
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from fastapi.middleware.cors import CORSMiddleware
import Lib.srs_models as srs_models
import Lib.libo2lsdb as o2lsdb
import Lib.libconnect as libconnect
from pydantic import BaseModel
import Lib.LiveHtml as LiveHtml

#All constants declaration
tz = 8 #声明时区UTC+8
site_url = site_settings.site_url
api_url = site_settings.api_url
live_url = site_settings.live_url
flushFlag = False


#program startups
app = FastAPI()


conn = libconnect.conn
cur = libconnect.cur
cur.execute('SELECT * FROM TOKENS ORDER BY TOKEN_NO DESC LIMIT 1;')#写死的SQL 没有风险
global TOKEN_NO
TOKEN_NO = cur.fetchone()#声明全局变量
TOKEN_NO = TOKEN_NO[0]#你可能会笑我 但是我就这么写了


#接入CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://10.0.10.3",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

requestsItemPublish = srs_models.requestsItemPublish
requestsItemConnect = srs_models.requestsItemConnect
requestsItemClose = srs_models.requestsItemClose
requestsItemUnpublish = srs_models.requestsItemUnpublish
requestsItemStop = srs_models.requestsItemStop
requestsItemPlay = srs_models.requestsItemPlay
requestsItemDvr = srs_models.requestsItemDvr

@app.get("/")#This is for main page
async def root():
    return "就不要研究人家API了好嘛！"

@app.get("/status")#this is for heartbeat to detect the client status
async def status_check(user_id: int, time_stamp: int ,status: bool):#接收状态信息
    return("status" , "OK")

@app.get("/ping")#this is for getting the ping of the server 
async def ping():
    return("status" , "OK")

@app.get("/login/")
async def read_item(username: str , password: str, time: str): #这里是登录API,主要实现功能是客户端点击login将get http://site.com/login/?username=2&password=2&time=200303031211
    #user_information = {"username": username,"password": password,"time":str}
    #进入登录验证部分
    real_pass = get_real_pass(password,time)

    result = o2lsdb.findByValue('USERS',o2lsdb.makeSelectIndex('user_id','auth','passwd'),'account',username)

    if not result == None: #登陆逻辑判断建议隐藏了因为我也不想看这一堆玩意
        if check_password_hash(result[2],real_pass):
            if result[1]=='ADMIN':
                login_admin_item = {"status" : "OK",
                "redirect_url" : site_url + '/web/Admin',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[1]),
                "tab" : 0
                }
                print(login_admin_item)
                return login_admin_item
            elif result[1]=='STUDENT':
                login_stu_item = {"status" : "OK",
                "redirect_url" : site_url + '/web/Student',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[1]),
                "tab" : 0
                }
                print(login_stu_item)
                return login_stu_item
            elif result[1]=='TEACHER':
                login_teacher_item = {"status" : "OK",
                "redirect_url" : site_url + '/web/Teacher',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[1]),
                "tab" : 0
                }
                print(login_teacher_item)
                return login_teacher_item
            else:
                pass
        else:
            return "AUTH_ERROR"
    else:
        return "AUTH_ERROR_NOUSER"

@app.get("/get_new_token")#刷新token用
async def flush(user_id: int , token: str):
    user_id = str(user_id)
    token = token.replace(' ','+')
    print(token)
    new_token = token_create(user_id,True,token)
    if new_token[1] == 'token_authentication_failure':
        return ("status","token_authentication_failure")
    else :
        back_item = {"status":"ok",
        "user_id" : user_id,
        "token" : new_token
        }#构造返回结构
        return back_item

@app.get("/check_valid")#用于程序传入数据的鉴权或者外部程序的回调等
async def check_valid(user_id: int , token: str):
    user_id = str(user_id)
    token = token.replace(' ','+')
    TOKEN_ITEM = o2lsdb.findByValue('TOKENS',o2lsdb.makeSelectIndex('user_id','name','auth'),'token',token)
    check_item = token_check(token)
    if TOKEN_ITEM==None :
        return("status" , "token_authentication_failure")
    elif not check_item == 'TOKEN VALID':
        return("status" , "token_authentication_failure")
    elif check_item == 'TOKEN VALID':
        result = o2lsdb.selectByID('USERS',o2lsdb.makeSelectLine('auth'),user_id,'user_id')
        if result == None:
            returnItem = {
                "status" : "token_authentication_failure"
            }
        else :
            returnItem = {
                "status" : "OK",
                "auth" : str.upper(result[6])
            }
        return(returnItem)
    else :
        return("status" , "token_authentication_failure")

@app.get("/logout")#销毁Token，登出
async def logout(user_id: int , token: str):
    user_id = str(user_id)
    token = token.replace(' ','+')
    
    TOKEN_ITEM = o2lsdb.findByValue('TOKENS',o2lsdb.makeSelectIndex('user_id','name','auth'),'token',token)

    check_item = token_check(token)
    if TOKEN_ITEM==None :
        return("status" , "logout_failed")
    elif not check_item == 'TOKEN VALID':
        return("status" , "OK")
    elif check_item == 'TOKEN VALID':
        o2lsdb.updateByID("USERS",o2lsdb.makeUpdateLine('expired',True),user_id,'user_id')
        return("status","OK")
    else :
        return("status" , "logout_failed")
    pass

@app.get("/mainpage")#这个API默认了user_id存在，后续可能会增加进一步的错误处理 patched
async def mainpage(token: str , user_id: int ):
    user_id = str(user_id)
    token = token.replace(' ','+')

    USER_ITEM = o2lsdb.selectByID('USERS',o2lsdb.makeSelectLine('name','grade','auth','last_course','exit_time','gender','intro','motto'),user_id,'user_id')
    check_item = auth_func(user_id,token)
    if USER_ITEM == None:
        return("status","AUTH_ERROR")
    else:
        if not check_item == 'TOKEN VALID':
            return("status","AUTH_ERROR")
        else :
            return_item = {
                "status" : "OK",
                'statistics' : {
                    "CPUS" : 12,
                    "Total_Usage" : 13,
                    "Per_Usage" : 52,
                    "Total_Mem" : 23 ,
                    "Free_Mem" : 23 
                },
                'information' : {
                    'name' : USER_ITEM[0],
                    'grade' : USER_ITEM[1],
                    'auth' : USER_ITEM[2],
                    'last_course': USER_ITEM[3],
                    'exit_time' : USER_ITEM[4],
                    'gender' : USER_ITEM[5],
                    'intro' : USER_ITEM[6],
                    'motto' : USER_ITEM[7]
                }
            }
            return return_item

@app.get("/get_main_content")
async def maincontent(token: str , user_id: int , section: int , page : int):
    user_id = str(user_id)
    token = token.replace(' ','+')
    result = totalAuth(user_id , token)
    if result == "TOKEN VALID":
        pass
    else :
        return("status" , "token_authentication_failure")

@app.get("/fetch_course_by_id")
async def fetch_course_by_id(token: str , user_id: int , course_id : int):
    user_id = str(user_id)
    course_id = str(course_id)
    token = token.replace(' ','+')
    result = totalAuth(user_id , token)
    if result == "TOKEN VALID":
        result = o2lsdb.selectByID('USERS',o2lsdb.makeSelectLine('class_id'),user_id,'user_id')
        class_id = str(result[0])
        print(class_id)
        result = o2lsdb.selectByID('COURSE',o2lsdb.makeSelectLine('visibility','title','people','listening','time_start','time_end','is_end'),course_id,'course_id')

        if not result == None:
            visibleFlag = False
            print(result)
            visibility = resolve_visibility(result[0])
            print(visibility)
            for item in visibility:
                if str(item) == class_id:
                    visibleFlag = True
                    break
                else:
                    pass

            if visibleFlag :
                print(result)
                returnItem = {
                    "status" : "OK",
                    "title" : result[1],
                    "people" : result[2],
                    "listening" : result[3],
                    "time_start" : result[4],
                    "time_end" : result[5],
                    "is_end" : result[6]
                }
                return returnItem
            else :
                return("status","invisible_to_current_user")
        else:
            return("status","course_id_invalid")
    else:
        return("status" , "token_authentication_failure")

@app.post('/srs_on_connect')
async def srs_on_connect(json : requestsItemConnect):
    if not json.app == 'live':
        return 1
    elif json.tcUrl.find('?') == -1 and json.tcUrl.find('&') == -1:
        return 2
    auth_list = json.tcUrl[json.tcUrl.find('?') + 1:len(json.tcUrl)].split('&')
    auth_dict ={}
    for tmp in auth_list:
        tmp2 = tmp.split('=',1)
        tmp3 = {tmp2[0]:tmp2[1]}
        auth_dict.update(tmp3)
    result = totalAuth(auth_dict.get('user_id',None) , auth_dict.get('token',None))
    if not result == 'TOKEN VALID':
        return 3
    else:
        result = o2lsdb.findByValue('TOKENS',o2lsdb.makeSelectIndex('user_id','auth'),'token',auth_dict.get('token',None))
        if not result[1] == 'TEACHER':
            return 4
        else :
            result = o2lsdb.findByValue('COURSES',o2lsdb.makeSelectIndex('course_id','is_end'),'course_id',str(json.stream))
            if not result[1] == False:
                return 0
            elif result == None:
                return 5
            else:
                return 6

@app.post('/srs_on_close')
async def srs_on_close(json : requestsItemClose):
    return 0

@app.post('/srs_on_publish')
async def srs_on_publish(json : requestsItemPublish):
    return 0

@app.post('/srs_on_unpublish')
async def srs_on_unpublish(json : requestsItemUnpublish):
    return 0

@app.post('/srs_on_play')
async def srs_on_play(json : requestsItemPlay):
    if not json.app == 'live':
        return 1
    elif json.param.find('?') == -1 and json.param.find('&') == -1:
        return 2
    auth_list = json.param[json.param.find('?') + 1:len(json.param)].split('&')
    auth_dict ={}
    for tmp in auth_list:
        tmp2 = tmp.split('=',1)
        tmp3 = {tmp2[0]:tmp2[1]}
        auth_dict.update(tmp3)
    result = totalAuth(auth_dict.get('user_id',None) , auth_dict.get('token',None))
    if not result == 'TOKEN VALID':
        return 3
    else:
        return 0
    
@app.post('/srs_on_stop')
async def srs_on_stop(json : requestsItemStop):
    print(json)
    print("Stop")
    return 0

@app.post('/srs_on_dvr')
async def srs_on_dvr(json : requestsItemDvr):    
    return 0

@app.get('/live')
async def live(user_id,token,course_id):
    return Response(content=LiveHtml.html[0] + live_url + '/live/' + course_id + '?user_id=' + user_id +'&token=' + token + LiveHtml.html[1], media_type="text/html")


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

#创建一个token 并初始化信息 同时，当上一个token存在的时候，将上一个token过期
#这里我使用了一个Flag表示函数是否由登陆函数调起，因为登陆时不会传入上一个token 即 如果第二个参数是False表示其由登陆函数拉起
def token_create(user_id,*args):
    global TOKEN_NO
    time = get_time_string() + '00'
    user_id = str(user_id)
    def makeTOKEN_STRING(user_id):
        ## A Stupid Function Used to make the TOKEN_STRING more random
        i = 0
        TOKEN_STRING = user_id[i] + str(random.randint(0,9))
        while i < len(user_id)-1:
            i = i + 1
            TOKEN_STRING = TOKEN_STRING + user_id[i] + str(random.randint(0,9))
        
        return TOKEN_STRING

    encrypted = str(generateMD5(makeTOKEN_STRING(user_id)))
    print(encrypted)
    while o2lsdb.securitySQL(encrypted) == 'Insecure' or not encrypted.find('/') == -1:##it seems that no do .. while loop in python ? and halt '/' as it will have some problem
        encrypted = str(generateMD5(makeTOKEN_STRING(user_id)))
    AUTH = o2lsdb.selectByID('USERS',o2lsdb.makeSelectLine('auth'),user_id,'user_id')

    if AUTH:
        AUTH = AUTH[0]
    else :
        pass

    if args[0] == True:#程序的这个分支保证token不会被恶意过期
        check_item = token_check(args[1])
        print(check_item)
        if check_item == 'ERROR TOKEN NOT EXIST' or check_item == 'TOKEN EXPIRED' or check_item == 'TOKEN TIME INVAID' :#如果传入的token并不存在或者已过期
            return ("info" , "token_authentication_failure")
        else :#如果传入的token和user_id对应
            if o2lsdb.securitySQL(user_id) == 0 or user_id.isdigit == True:
                sql = "SELECT * FROM TOKENS WHERE USER_ID = '" + user_id + "'" + " ORDER BY TOKEN_NO DESC LIMIT 1 "
                cur.execute(sql)
                token_user = cur.fetchone()
                if token_user[3] == args[1]:
                    o2lsdb.updateByID("TOKENS",o2lsdb.makeUpdateLine('expired','True'),user_id,'user_id')
                else :
                    AUTH = None
            else:
                return ("info" , "token_authentication_failure")

    else :
        TOKEN_ITEM = o2lsdb.selectByID('TOKENS',o2lsdb.makeSelectLine('token_no','expired'),user_id,'user_id')
        if TOKEN_ITEM == None :#如果该用户上一个TOKEN不存在
            pass
        else :#当上一个token存在的时候expire它
            o2lsdb.updateByID("TOKENS",o2lsdb.makeUpdateLine('expired','True'),user_id,'user_id')
    if AUTH == None:
        return ("info" , "token_authentication_failure")
    else :
        o2lsdb.insertFulline('TOKENS',o2lsdb.makeInsertLine(TOKEN_NO + 1,time,'False',encrypted,user_id,AUTH))
        TOKEN_NO = TOKEN_NO + 1 #注意这里将初始化时的TOKEN_NO加一，表示添加了一条记录
        return encrypted

def token_check(token):#检查token有效性无非3样，token不存在，键值记录的token确已过期，token时间已经过期，如果三种验证都pass了，token就有效
    TOKEN_ITEM = o2lsdb.findByValue('TOKENS',o2lsdb.makeSelectIndex('token_no','expired','time_created'),'token',token)
    if TOKEN_ITEM == None :#如果token不存在，抛出异常
        return 'ERROR TOKEN NOT EXIST'
    elif TOKEN_ITEM[1] == True :
        return 'TOKEN EXPIRED'
    elif token_is_valid(TOKEN_ITEM[2][:14]):#最复杂的部分，由于数据库时间为16位
        return 'TOKEN TIME INVAID'
    else :
        return 'TOKEN VALID'


def generateMD5(str):
    return(hashlib.new('md5',str.encode('utf-8')).hexdigest())

def get_time_string():#这是一个获取当前时间字符串格式的函数（精确到秒
    localtime = time.localtime(time.time())
    time_entity = time.strftime("%Y%m%d%H%M%S",localtime)
    return time_entity

def fmt_time(time_string): #返回时间元组和时间戳
    stamp = str(time.mktime(time.strptime(time_string,"%Y%m%d%H%M%S")))
    return stamp

def token_is_valid(token_create_time):#检查TOKEN是否已经过时的函数
    ts1 = fmt_time(token_create_time)
    #print(str(ts1))
    ts2 = fmt_time(get_time_string())
    #print(str(ts2))
    if 0 < float(ts1) - float(ts2) < 3600 :
        return True
    else :
        return False

def auth_func(user_id,token):#不打算更改已经写的代码了，这里抄一份改改
    user_id = str(user_id)
    token = token.replace(' ','+')
    TOKEN_ITEM = o2lsdb.findByValue('TOKENS',o2lsdb.makeSelectIndex('time_created','expired','user_id'),'token',token)
    print(TOKEN_ITEM)
    if TOKEN_ITEM == None :#如果token不存在，抛出异常
        return 'ERROR TOKEN NOT EXIST'
    elif TOKEN_ITEM[1] == True :
        return 'TOKEN EXPIRED'
    elif token_is_valid(TOKEN_ITEM[0][:14]):#最复杂的部分，由于数据库时间为16位
        return 'TOKEN TIME INVAID'
    elif not TOKEN_ITEM[2] == int(user_id):
        return 'ID TOKEN NOT MATCH'
    else :
        return 'TOKEN VALID'
    pass

def resolve_visibility(visibility):#返回可见课程的列表组
    visibility = str(visibility)#强制类型转换
    resolved = visibility.split("/s",-1)
    return resolved

def totalAuth(user_id , token):#总鉴权函数 根据传入信息决断状态
    token = token.replace(' ','+')
    TOKEN_ITEM = o2lsdb.findByValue('TOKENS',o2lsdb.makeSelectIndex('user_id'),'token',token)
    check_item = token_check(token)
    if TOKEN_ITEM==None :
        return "TOKEN DOES NOT EXIST"
    elif not check_item == 'TOKEN VALID':
        return "TOKEN INVAILD"
    elif check_item == 'TOKEN VALID':
        result = o2lsdb.findByValue('USERS',o2lsdb.makeSelectIndex('user_id','grade'),'user_id',user_id)
        if result == None:
            return "USER_ID INVALID"
        else :
            return "TOKEN VALID"
    else :
        return "FATAL ERROR ENCOUNTERED"
