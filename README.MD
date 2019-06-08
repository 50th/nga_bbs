#BBS

---
开发环境：

Python 3.7

Django 2.2

没有使用pymysql，用的mysqlclient 1.4.2

---
主页展示：
    --热帖

板块展示：
    --发帖

帖子显示：
    --评论，显示二级评论

权限管理：
    --用户-角色-权限
    
    根据url和method判断是否具有权限；
    使用from django.urls import resolve，得到url_name
---
res_msg = {
"status":False,
"code":0,
"msg":"",
}

status:True or False

code:

    0:显示msg
    1：跳转

msg:错误信息 or 跳转的url 
