# OpenOLS

The project OpenOLS is a new , light , fast OnLine Studtying system .

# For developers

我们有`dev.sunboy.site`作为本地服务器的前端地址，`api.sunboy.site`作为api的地址（不支持WebSocket）。

## Lisence 

This project is capable under MIT Lisence.

## Key functions

# 1.学生

## 1.主页

主页应该展示学生的基础个人信息，基础统计情况（？），同学的在线人数（没卵用），服务器信息（内存什么的的占用？），一句哲言？，特性介绍（滚动，这个很关键），搞个大的聊天室可以玩玩（严格限制发言频率）。

## 2.直播课程

课程的列表，每个课程显示授课老师和在线人数，起止时间，课程的标题，课程的封面（默认或者老师上传）。老师如果在直播课中选择了全程录像，那么OpenOLS会记录你的离开时间（如果你有什么事物去办），并在直播回放中自动定位到该时间，但是如果你中途退出又进入，就会导致之前的回放定位被覆盖。

## 3.录播课程

课程的列表，每个课程显示授课老师，课程的标题，课程的封面（默认或者老师上传），已看人数。

## 4.资源中心

按格式分区，按时间排序，可以接受一个小于30字的附加说明。比如：
```
PDF

20200402英语课件.pdf
20200402化学课本.pdf

MP4

20200428物理实验视频.mp4

PPTX（PPT）

某一日的讲义.ppt
```

## 5.收藏夹（核心功能 ，很帅

可以对服务器上的任何资源，包括 Fusion Share 和 Time Line 进行标记，使其进入收藏夹，随时进入收藏夹。如果对一个直播课进行标记，该课程回放生成之后，课程回放进入收藏夹。

第一次进行的标记会使标记资源进入缓冲区，如果不点击永久化就会在一定时间中删除。永久化可以进入各个子收藏夹，文件结构类似

```

收藏夹---缓冲区------语文
                |
                |---美文
                |
                |---音乐
                |
                |---点子

```

## 6.Time Line （刚刚受到达芬奇的启发 很酷 但是也比较难实现  非常喜欢这个点子

这个界面可以给自己添加一条时间线（以天，年，月之类的为周期，在某个时间加入一个时间点，创建一个备注，创建完后讲按照类似剪辑软件中的时间线的形式呈现（一个游标，一些标记，鼠标悬浮或者屏幕点击到标记上的时候，显示这个时间点的备注。），可以对已经到时间的节点打勾表示完成。（对于三种角色都有意义）

同时，老师、管理员也可以选择对哪个班级创建一个时间线。在学生侧可见创建者名字等等。

同时Time Line区分 aroll和broll，类似剪辑中的ab部分概念，根据优先级管理事件。

## 7.Fusion Share

这个界面学生或者老师或者管理员可以PO一篇文章，一张图片，一段声音，或者一个链接，但是不可以是视频。并且可以在内容下添加一条不超过50个字的注解。可以分享学习资料，分享学习心得，分享自己的笔记，可以选择匿名。但是超级管理员可以看到你的姓名，并对不合适的内容进行删除。

Share的内容可以是站内的收藏夹，或者自己的 Time Line 和 Reminder。

## 8.Reminder

一个点子会突然出现在你的脑海，但是如果你没抓住它，它也许就永远消失了。在一个灵感迸发的时候，打开OpenOLS，以一个便签的形式记录下来它。你可以不先起标题而只记录你的点子。在便签里，形式就不再受到严格的限制，这是个“浮动”标签，你可以记录一段文字，一段语音。但是OpenOLS不会提醒你关于其的任何信息，你可以自行查看而不受打扰。

## 9.Power Halt

OpenOLS秉持着开放的心态，不会逼着朋友们去学习，你可以给自己设置一个合理的Halt时间，在这个时间中，你不能访问OpenOLS除了直播课以外的其他内容，从而获得一个小憩。同时OpenOLS也在你点下返回或者退出或者重新登陆之时取消你的Halt状态。

## 5.家庭作业（作业和测试的计划推迟，交给智学网

## 6.测试中心

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

进入门户`https://site.com`显示登录界面，有两个输入框，用户名，密码，自动跳转 `学生 教师 管理员`。
学生正常登录，被重定向到`https://site.com/student_area`能看见所属班级，班级人数，同学列表，直播课程，课件列表，直播回放，录播课程。
同学点击任何功能进入。

### 老师

进入门户`https://site.com`显示登录界面，有两个输入框，用户名，密码，自动跳转 `学生 教师 管理员`。
老师正常登录，被重定向到`https://site.com/teacher_area`能看见所教班级，点选几个班级上传课件，点选几个班级开始直播，点选几个班级上传录播录像。

## 管理员

进入门户`https://site.com`显示登录界面，有两个输入框，用户名，密码，自动跳转 `学生 教师 管理员`。
老师正常登录，被重定向到`https://site.com/administrator_area`能看见各个年级，增添人员，删除人员，管理资源（全部），同时应该有批量删除，批量导入csv,批量导出csv的功能。


## Data Structure

Tips：数据结构设计要谨慎，仔细根据功能考虑。

```

---------------------------------

    pgsql-----DB1-----public
                        | 
                        | #tables
                        |--users
                        |
                        |--course
                        |
                        |--locations
                        |
                        |--resources
                        |
                        |--tokens

---------------------------------

For Table Users

+--------+-------+-------+---------+---------+--------+--------+--------+
| USER_ID| NAME  | GRADE | CLASS_ID| CHAT_ID | PASSWD | AUTH   | ACCOUNT|
+--------+-------+-------+---------+---------+--------+--------+--------+
|90155664|吴此仁  | 2018  | 201815  |885823  |17ac5be | STUDENT| 114514  |
-------------------------------------------------------------------------

续表

+-----------+--------------+-------+---------+---------+
|LAST_COURSE|EXIT_TIME     |GENDER |INTRO    |MOTTO    |
+-----------+--------------+-------+---------+---------+
|00000001   |20200418220000|男     |并不存在的|并无格言  |
--------------------------------------------------------


---------------------------------

For Table Course

+---------+-----------------+--------+------------+---------+----------------+----------------+----------+
|COURSE_ID| TITLE           | PEOPLE | VISIBILITY |LISTENING|TIME_START      |TIME_END        |IS_END    |
+---------+-----------------+--------+------------+---------+----------------+----------------+----------+
|00000001 |从不存在的一节网课 | 45     | 1\s2\s3\s  |25       |20200405205735  |20200405220000  |True      |
---------------------------------------------------------------------------------------------------------- 

---------------------------------

For Table Locations

+---------+--------------+-------------+----------------------+
|COURSE_ID| RTMP_URL     |CHAT_URL     | BOARD_URL            | 
+---------+--------------+-------------+----------------------+
|00000001 |rtmp://a.com/1| ws://a.com/1| https://a.com/a.html |
---------------------------------------------------------------

---------------------------------

For Table Resources

+------------+-------+---------+-----------------------------+-----------+----------+--------+
|RESOURCE_ID |TYPE   |FILE_NAME|URL                          |VISIBILITY |FILE_OWNER|OWNER_ID|
+------------+-------+---------+-----------------------------+-----------+----------+--------+
|000000000001|MP4    |TokyoCold|https://a.com/tokyocold.mp4  |1\s2\s\14\s|Teacher1  |99999997|
----------------------------------------------------------------------------------------------

续表

+--------+--------------+------------------+-----------+
|INTRO   |UPLOAD_TIME   |COVER_URL         |SIZE       |
+--------+--------------+------------------+-----------+
|A video |20200429171400|http://a.com/a.jpg|13550014   |
--------------------------------------------------------

---------------------------------

For Table Tokens

+--------+--------------+---------+-----------+----------+-----+
|Token_NO| Time_CREATED | EXPIRED | TOKEN     | USER_ID  |AUTH |
+--------+--------------+---------+-----------+----------+-----+
|0000001 |20200418220000| False   | 39e9e146c9| 90155664 |admin|
----------------------------------------------------------------

---------------------------------


```
