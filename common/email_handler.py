import smtplib
from email.mime.text import MIMEText


# smtp_server = 'smtp.163.com'  # 服务器地址
# from_user = "qq754514192@163.com"  # 用户名
# user_pass = 'hewei20124661'  # 密码
# receivers = ['754514192@qq.com',]  # 收件人

# message = MIMEText('测试发送内容', 'plain', 'utf-8')  # 发送的消息对象
# message['Subject'] = '测试'  # 主题
# message['From'] = from_user  # 发件人
# message['To'] = receivers[0]  # 收件人
#
# smtp_obj = smtplib.SMTP()
# smtp_obj.connect(smtp_server, 25)  # 连接服务器
# smtp_obj.login(from_user, user_pass)  # 登录
# smtp_obj.sendmail(from_user, receivers, message.as_string())  # 发送
# smtp_obj.quit()  # 退出

smtp_info = {
    "smtp_host": 'smtp.163.com',
    'port': 25,
    "username": 'qq754514192@163.com',
    'password': 'hewei20124661',
}


def send_email(reveiver, subject, msg):
    smtp_host = smtp_info['smtp_host']
    smtp_port = smtp_info['port']
    username = smtp_info['username']
    password = smtp_info['password']

    message = MIMEText(msg, 'plain', 'utf-8')  # 发送的消息对象
    message['Subject'] = subject  # 主题
    message['From'] = username  # 发件人
    message['To'] = reveiver  # 收件人
    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(smtp_host, smtp_port)  # 连接服务器
        smtp_obj.login(username, password)  # 登录
        smtp_obj.sendmail(username, [reveiver,], message.as_string())  # 发送
        smtp_obj.quit()  # 退出
        return True
    except Exception as e:
        return False
