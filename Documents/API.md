# 这是一份关于API的文档

### 注：传入参数中`user_id : int`冒号前指一个简述的参数信息，后边指该信息的类型。

## 写在前面

1.USER_ID是指系统内部的ID，USERNAME是指登陆账号，相应的是数据库中的ACCOUNT。
2.可能会有一些令人混淆，如果有一个用户名字叫student，他的权限也是”学生“，但是通过API获取的user_name会是小写，auth会是全都是大写。即auth:"ADMIN"


## 地址 `/`
```
返回一条信息，不要研究人家API辽
```

## 地址`/status`
```
传入：user_id: int, time_stamp: int ,status: bool
传回:["status" , "OK"]
参数解释:
API功能：Heartbeat来检测客户端状态的
```

## 地址`/ping`
```
传入：无
传回：["status" , "OK"]
参数解释：无
API功能：获取到服务器延时的API
```

## 地址`/login/`
```
传入：username: str , password: str, time: str
传回：
    1.当身份验证失败时返回 AUTH_ERROR
    2.当身份验证成功时返回 json1①
参数解释：username: str 用户名 , password: str 密码 , time: str 当前时间指 var myDate = new Date();var Sec = myDate.getSeconds(); 中的Sec

①{"status" : "OK",
  "redirect_url" : "http://dev.sunboy.site/admin",
  "user_id" : 90155664
  "token" : "5a39e9e146c9"
  "AUTH" : "ADMIN",
  "tab" : 0//前端可以忽略，因为没P用哈哈哈哈
 } // 解释起来大概是状态OK，将被重定向到 $url 带有token 5a39e9e146c 身份是 ADMIN 打开tab 0
注意：redirect_url可以根据auth变化，或者统一，再由前端判断。
```

## 地址`/get_new_token`
```
传入：user_id: int , token: str
传回：
    1.当鉴权成功的时候（user_id与token对应，且token的创建日期早于目前客户端日期（防止改日期复用token，获取一个与user_id相对的新token，同时旧的token会被标记为失效。
    2.当鉴权失败的时候（上述条件任一不符合），返回token_authentication_failure
参数解释：user_id: int 用户ID , token: str 登录时获取的token或者从本API获取的上一个token。注意！ 一旦新的token被注册，上一个token会立刻失效。
{
  "status" : "OK",//或者可能是token_authentication_failure
  "user_id" : 90155664//传回user_id，请double check ID是否正确。
  "token" : "5a39e9e14129"//调用此API时注意，如果登陆时获取了权限是ADMIN，那新的ID也自动是ADMIN作为token权限。
}
```

## 地址`check_valid`
```
传入：user_id: int , token: str
传回：
    1.当鉴权成功的时候（user_id与token对应，且token的创建日期早于目前客户端日期（防止改日期复用token，获取一个与user_id相对的新token，同时旧的token会被标记为失效。
    2.当鉴权失败的时候（上述条件任一不符合），返回token_authentication_failure
参数解释：user_id: int 用户ID , token: str 登录时获取的token或者从本API获取的上一个token。
{
  "status" : "OK",//或者可能是token_authentication_failure
}
```

## 地址`/logout`
```
传入：user_id: int , token: str
传回：
    1.当鉴权成功的时候，（user_id与token对应，且token的创建日期早于目前客户端日期（防止改日期复用token。
    2.鉴权失败的时候抛出 logout_failed 。
{
  "status" : "OK",//或者可能是logout_failed
  "auth" : "STUDENT"//三种角色
}

```

## 地址`/mainpage`
```
传入：user_id: int , token: str
传回：
    1.鉴权成功返回信息。
    2.鉴权失败返回信息 AUTH_ERROR 。
{
  "status" : "OK",
  'statistics' : {
    "CPUS" : logical,
    "Total_Usage" : percent,
    "Per_Usage" : per_percent,//返回数组，不用可以丢弃
    "Total_Mem" : total ,
    "Free_Mem" : free 
  },
  'information' : {
    'name' : USER_ITEM[1],
    'grade' : USER_ITEM[2],
    'auth' : USER_ITEM[6],
    'last_course': USER_ITEM[8],
    'exit_time' : USER_ITEM[9],
    'gender' : USER_ITEM[10],
    'intro' : USER_ITEM[11],
    'motto' : USER_ITEM[12]
  } //这些information的具体信息请看英文意思和数据结构
}
```

## 地址`/get_main_content`
```
传入：token: str , user_id: int , section: int , page : int
传回：
    1.当鉴权成功的时候（user_id与token对应，token未过期），返回需要显示的主要内容
    2.当鉴权失败的时候返回 AUTH_ERROR
    3.如果需要获取的section超出范围，返回错误信息SECTION_INVALID
    4.如果需要获取的page超出范文，返回错误信息PAGE_INVALID
参数解释：user_id: int 用户ID , token: str 登录时获取的或者从 get_now_token获取的上一个token。
API调用错误：AUTH_ERROR , SECTION_INVALID , PAGE_INVALID
成功示例：
{
  "status" : "OK",
  "section" : "stream",//下附section表
  "page" : "1",//为了方便人类阅读，page的起始页是1
  "content" : {
    "col1" : {
      "title" : "一节从来不存在的网课",
      "people" : 45,
      "listening" : 25,
      "time_start" : "20200405205735",
      "time_end" : "20200405220000",
    }
    "col2" :{
      "title" : "第二节从来不存在的网课",
      "people" : 42,
      "listening" : 20,
      "time_start" : "20200405205735",
      "time_end" : "20200405220000",
    }
    "col3" : null, //Json里应该没有None
  }
}
失败示例：
{
  "status" : "AUTH_ERROR",
}

注意：此API获取数据，根据section和page进行定位。

section表
+---+--------------+
|1  |直播课程       |
+------------------+
|2  |录播课程       |
+------------------+
|3  |收藏夹         |
+------------------+
|4  |FusionShare   |
+------------------+
|5  |Reminder      |
+------------------+
|6  |TimeLine      |
+------------------+
```
## 地址`/get_live_addr`
```
传入：token: str , user_id: int , course_id: int
传回：
    1.鉴权基本同前。
    2.传回rtmp_url , chat_url , board_url。分别是直播流地址，聊天室地址，黑板url。
    3.由于实现起来过于蛋疼，忽略board_url吧。
API调用错误：token_expired , course_not_exist , token_not_match , server_error , user_not_in_class（这个课程在数据库存在，但用户所在的班级并不是课程面向的班级 ，一般情况下这个错误并不会出现，因为错误的course_id不回被返回到前端去，只是为了防止有人硬改）, course_ended ,（同上，一般不会出现） , course_not_started（可能会出现，因为预定要上的课也会被返回前端），user_multi_course （一次正确的调用API会导致该直播间人数+1，同时刷新用户的 'IS_ONLINE"状态，如果该用户的 'IS_ONLINE'是True，则会返回本信息，禁止一个用户同时上两门课。如果上一节课退出，服务器会在15秒钟内探测到并重置该用户的 'IS_ONLINE'状态，同时如果课程到达时间，该状态也会被重置） 。
失败示例基本同上
成功示例：
[
  "status" : "OK",
  "rtmp_url" : "rtmp://site.com/live/cid12849752",
  "chat_url" : "ws://site.com/cid12321944",
  "board_url" : "http://example.com" //这项没鸡儿用
]
```

## 地址`/get_static_resourse`
```
传入：token: str , user_id: int , course_id: int
传回：
    1.鉴权基本同前。
    2.鉴权错误传回AUTH_ERROR。
    3.
```