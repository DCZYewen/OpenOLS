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
参数解释：username: str 用户名 , password: str 密码 , time: str 当前时间指 var myDate = new Date();var Sec = myDate.getSeconds(); 中的Sec
```