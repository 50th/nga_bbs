import smtplib
from email.mime.text import MIMEText


smtp_info = {
    "smtp_host": 'smtp.163.com',
    'port': 25,
    "username": '******@163.com',
    'password': '********',
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
