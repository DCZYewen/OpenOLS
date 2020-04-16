# OpenOLS

The project OpenOLS is a new , light , fast Online Coursing system .

# For developers

我们有`dev.sunboy.site`作为本地服务器的前端地址，`api.sunboy.site`作为api的地址（不支持WebSocket）。

## Lisence 

This project is capable under MIT Lisence.

## Key functions

1.账户权限管理，同平台登录，管理员添加人员之类。

2.内容管理，老师可以开课，学生可以上课。

3.适配手机UI。

4.课件上传，课件在线预览。

5.非实时视频

    播放

    允许下载视频

    弹幕

    显示观看进度，禁止拖拽进度条到观看进度以后的位置

    防止挂机
       
       非活动标签页时暂停播放
       
    分为必修和选修

6.实时视频

    播放

    直播回看  

    课堂内教师同学等实时互动
    
    防止挂机
    
        建立学生在线统计表，离线时黑色，非活动标签页时红色，挂机时黄色（判断机制？），正常时绿色

    直播模式选择

        --老师用手机直播，直推摄像头画面
        --老师用PC直播，采集摄像头和板书（PPT之类
        
7.测试

    包括题型：单选，多选，填空，简答。由老师设置题目，客观题自动判分，主观题手动判分。

    禁止复制网页文字，如果试图复制，弹窗或将复制的文字替换为“警告”

## Statements of How to achieve

1.前后端分离 前端使用H5 CSS HTML构建

    1.直播流服务器后端采用SRS
    2.推送端输出端都使用rtmp协议。
    3.前端播放直播流采用flv.js，使用h5技术播放rtmp流，最可以降低延迟。

2.前后端分离 后端使用fastapi构建一个统一的API系统，前端的作用是发出请求，数据由后端API提供，再由前端格式化。

3.数据库采用postgresql，使用fastapi访库。就基本把fastapi作为一个中间件，作为沟通前端和数据库的桥梁。

## Text Statements Of A Tour 

`本部分使用site.com作为站点url`

### 学生

进入门户`https://site.com`显示登录界面，有两个输入框，用户名，密码，三个选择可选 `学生 教师 管理员`。
学生正常登录，被重定向到`https://site.com/student_area`能看见所属班级，班级人数，同学列表，直播课程，课件列表，直播回放，录播课程。
同学点击任何功能进入。

### 老师

进入门户`https://site.com`显示登录界面，有两个输入框，用户名，密码，三个选择可选 `学生 教师 管理员`。
老师正常登录，被重定向到`https://site.com/teacher_area`能看见所教班级，点选几个班级上传课件，点选几个班级开始直播，点选几个班级上传录播录像。

## 管理员

进入门户`https://site.com`显示登录界面，有两个输入框，用户名，密码，三个选择可选 `学生 教师 管理员`。
老师正常登录，被重定向到`https://site.com/administrator_area`能看见各个年级，增添人员，删除人员，管理资源（全部），同时应该有批量删除，批量导入csv,批量导出csv的功能。


## Data Structure

Tips：数据结构设计要谨慎，仔细根据功能考虑。

```

---------------------------------

    -----postgresql
       | 
       | #tables
       |--users
       |
       |--course
       |
       |--locations
       |
       |--classes
       |
       |--

---------------------------------

For Table Users

+--------+-------+-------+---------+---------+--------+----------+--------+--------+
| USER_ID| NAME  | GRADE | CLASS   | CHAT_ID | PASSWD | IS_ONLNE | AUTH   | ACCOUNT|
+--------+-------+-------+---------+---------+--------+----------+--------+--------+
|90155664|李子豪  | 2018  | 15      |885823   |17ac5be | False   | STUDENT| 114514  |
-----------------------------------------------------------------------------------+

---------------------------------

For Table Course

+---------+-----------------+--------+------------+---------+----------------+----------------+
|COURSE_ID| TITLE           | PEOPLE | CLASS_IN   |LISTENING|TIME_START      |TIME_END        |
+---------+-----------------+--------+------------+---------+----------------+----------------+
|00000001 |从不存在的一节网课| 45      | 1\s2\s3\s4 |25      |20200405205735  |20200405220000  |
-----------------------------------------------------------------------------------------------

---------------------------------

For Table Locations

+---------+--------------+-------------+----------------------+
|COURSE_ID| RTMP_URL     |CHAT_URL     | BOARD_URL            | 
+---------+--------------+-------------+----------------------+
|00000001 |rtmp://a.com/1| ws://a.com/1| https://a.com/a.html |
---------------------------------------------------------------

---------------------------------

For Table Classes

+--------+-------+---------+---------+
|Class_ID| GRADE | CLASS   | MEMBERS |
+--------+-------+---------+---------+
|201815  |2018   | 15      | 45      |
--------------------------------------

---------------------------------

```
