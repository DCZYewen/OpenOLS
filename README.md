# OpenOLS

The project OpenOLS is a new , light , fast Online Coursing system .

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
    放挂机
6.实时视频
    播放
    直播回看  
    课堂内教师同学等半实时互动
    直播模式选择
        --老师用手机直播，直推摄像头画面
        --老师用PC直播，采集摄像头和板书（PPT之类

## Statements of How to achieve

1.前后端分离 前端使用H5 CSS HTML构建

    1.直播流服务器后端采用NginX
    2.推送端输出端都使用rtmp协议。
    3.前端播放直播流采用flv.js，使用h5技术播放rtmp流，最可以降低延迟。

2.前后端分离 后端使用fastapi构建一个统一的API系统，前端的作用是发出请求，数据由后端API提供，再由前端格式化。

3.数据库采用postgresql，使用fastapi访库。就基本把fastapi作为一个中间件，作为沟通前端和数据库的桥梁。

## Data Structure

Tips：数据结构设计要谨慎，仔细根据功能考虑。

