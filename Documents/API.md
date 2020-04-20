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

①["status" : "OK",
  "redirect_url" : "http://dev.sunboy.site/admin",
  "user_id" : 90155664
  "token" : "5a39e9e146c9"
  "auth" : "ADMIN",
  "tab" : 0//前端可以忽略，因为没P用哈哈哈哈
] // 解释起来大概是状态OK，将被重定向到 $url 带有token 5a39e9e146c 身份是 ADMIN 打开tab 0

```

## 地址/get_new_token
```
传入：user_id: int , token: str
传回：
    1.当鉴权成功的时候（user_id与token对应，且token的创建日期早于目前客户端日期（防止改日期复用token。
    2.当鉴权失败的时候（上述条件任一不符合），返回token_authentication_failure
参数解释：user_id: int 用户ID , token: str 登录时获取的token或者从本API获取的上一个token。注意！ 一旦新的token被注册，上一个token会立刻失效。
["status" : "OK",//或者可能是token_authentication_failure
  "user_id" : 90155664//传回user_id，请double check ID是否正确。
  "token" : "5a39e9e14129"//调用此API时注意，如果登陆时获取了权限是ADMIN，那新的ID也自动是ADMIN作为token权限。
]
```