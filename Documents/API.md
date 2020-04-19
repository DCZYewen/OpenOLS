# 这是一份关于API的文档

### 注：传入参数中`user_id : int`冒号前指一个简述的参数信息，后边指该信息的类型。

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
  "token" : "5a39e9e146c9"
  "auth" : "admin",
  "tab" : 0
} // 解释起来大概是状态OK，将被重定向到 $url 带有token 5a39e9e146c 身份是 admin 打开tab 0
```