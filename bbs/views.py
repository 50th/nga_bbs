from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.conf import settings
from bbs_models import models
import json
from common import valid_code, email_handler, md5handler


def login_reqiure(func):
    def inner(*args, **kwargs):
        request = args[0]
        username = request.COOKIES.get("username")
        password = request.COOKIES.get("password")
        user = models.UserProfile.objects.filter(username=username, password=password).first()
        if not user:
            username = request.session.get("username")
            password = request.session.get("password")
            user = models.UserProfile.objects.filter(username=username, password=password).first()
        if not user:
            return redirect("bbs:login")
        return func(*args, **kwargs)
    return inner


def index(request):
    user_obj = get_user_obj(request)
    forum_list = models.Forum.objects.all()
    return render(request, "bbs/index.html", {"user_obj": user_obj, "forum_list": forum_list})


def user_login(request):
    next_page = request.GET.get("next")  # 获取登录成功后的跳转页
    if not next_page:  # 如果没有，默认为到首页
        next_page = reverse("bbs:index")
    if request.method == "POST":
        username_type = request.POST.get("type")  # 用户输入的用户名类型，email，phone，用户名
        username = request.POST.get("username")
        password = request.POST.get("password")
        code = request.POST.get("validCode")  # 验证码
        keep_login = request.POST.get("keepLogin")  # 保持登录
        login_msg = {}
        if code == request.session["valid_code"]:
            password = md5handler.md5_convert(password, settings.PASSWORD_SALT)
            if username_type == "email":
                user = models.UserProfile.objects.filter(email=username, password=password).first()
            elif username_type == "mobail":
                user = models.UserProfile.objects.filter(phone=username, password=password).first()
            else:
                user = models.UserProfile.objects.filter(username=username, password=password).first()
            if user:
                request.session["username"] = user.username  # 存入session
                request.session["password"] = user.password
                login_msg["status"] = True
                login_msg["msg"] = "ok"
                login_msg["next"] = next_page
                ht = HttpResponse(json.dumps(login_msg))
                if keep_login == "true":  # 存入cookies
                    ht.set_cookie("username", user.username)
                    ht.set_cookie("password", user.password)
                return ht
            else:
                login_msg["status"] = False
                login_msg["msg"] = "用户名或密码错误"
                return HttpResponse(json.dumps(login_msg))
        else:
            login_msg["status"] = False
            login_msg["msg"] = "验证码错误"
            return HttpResponse(json.dumps(login_msg))
    else:
        # 确认cookies，session中是否保存有登录状态
        username = request.COOKIES.get("username")
        password = request.COOKIES.get("password")
        user = models.UserProfile.objects.filter(username=username, password=password).first()
        if not user:
            username = request.session.get("username")
            password = request.session.get("password")
            user = models.UserProfile.objects.filter(username=username, password=password).first()
        if user:
            return redirect(next_page)
        return render(request, "bbs/account_login.html", {"next_page": next_page})


@login_reqiure
def user_logout(request):
    request.session.flush()
    re = redirect("index")
    re.delete_cookie("username")
    re.delete_cookie("password")
    return re


def get_valid_code(request):
     v = valid_code.ValidCodeHandler(100, 34)
     code, img_data = v.get_valid_img()
     request.session["valid_code"] = code.lower()
     return HttpResponse(img_data)


@login_reqiure
def user_info(request):
    return HttpResponse("userinfo")


def user_register(request):
    if request.method == "POST":
        res_msg = {}
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")
        email = request.session.get("email")
        valid = request.POST.get("valid")
        user = models.UserProfile.objects.filter(username=username).first()
        if user:
            res_msg["status"] = False
            res_msg["error_code"] = "Username"
            res_msg["msg"] = "用户名已存在"
        elif valid != request.session.get("register_code"):
            res_msg["status"] = False
            res_msg["error_code"] = "Valid"
            res_msg["msg"] = "验证码输入错误"
        elif len(password)<6:
            res_msg["status"] = False
            res_msg["error_code"] = "Password"
            res_msg["msg"] = "密码过短"
        elif password != confirm_password:
            res_msg["status"] = False
            res_msg["error_code"] = "ConfirmPassword"
            res_msg["msg"] = "两次密码不一致"
        else:
            salt = settings.PASSWORD_SALT
            password = md5handler.md5_convert(password, salt)
            user = models.UserProfile.objects.create(username=username, password=password, email=email)
            user.save()
            request.session["username"] = user.username
            request.session["password"] = user.password
            res_msg["status"] = True
            res_msg["msg"] = "/bbs/"
            ht = HttpResponse(json.dumps(res_msg))
            ht.set_cookie("username", user.username)
            ht.set_cookie("password", user.password)
            return ht
        return HttpResponse(json.dumps(res_msg))
    else:
        return render(request, "bbs/account_register.html")


def send_register_code(request):
    res_msg = {"status": True}
    email = request.GET.get("email")
    user = models.UserProfile.objects.filter(email=email).first()
    if user:
        res_msg["status"] = False
        res_msg["error_code"] = "Email"
        res_msg["msg"] = "邮箱已注册"
    else:
        v = valid_code.ValidCodeHandler()
        code = v.get_valid_code()
        print(email, code)

        request.session['register_code'] = code
        request.session['email'] = email

        # res = email_handler.send_email(email, '注册验证码', code)
        # if res:
        #     request.session['register_code'] = code
        #     request.session['email'] = email
        #     res_msg["status"] = True
        # else:
        #     res_msg["status"] = False
        #     res_msg["error_code"] = "e"
        #     res_msg["msg"] = "请确认邮箱地址"
    return HttpResponse(json.dumps(res_msg))


def forums(request, *args, **kwargs):
    forum_id = kwargs.get("forum_id")
    forum_obj = models.Forum.objects.filter(id=forum_id).first()
    if forum_obj:
        page = request.GET.get("page")
        if page:
            page = int(page) if page.isdecimal() else 1
        else:
            page = 1
        print(page)
        user_obj = get_user_obj(request)
        forum_list = models.Forum.objects.all()
        return render(request, "bbs/forums.html", locals())
    else:
        return redirect("bbs:index")


class TopicView(View):
    def get(self, request, *args, **kwargs):
        topic_id = kwargs.get("topic_id")
        topic_obj = models.Topic.objects.filter(id=topic_id).first()
        print(topic_id)
        forum_list = models.Forum.objects.all()
        if topic_obj:
            page = request.GET.get("page")
            if page:
                page = int(page) if page.isdecimal() else 1
            else:
                page = 1
            pass
        elif topic_id:
            return redirect("bbs:index")
        else:
            username = request.COOKIES.get("username")
            password = request.COOKIES.get("password")
            user = models.UserProfile.objects.filter(username=username, password=password).first()
            if not user:
                username = request.session.get("username")
                password = request.session.get("password")
                user = models.UserProfile.objects.filter(username=username, password=password).first()
            if not user:
                url = reverse("bbs:login") + "?next=" + reverse("bbs:topic")
                return redirect(url)
            return render(request, "bbs/add_topic.html", {"user_obj": user, "forum_list": forum_list})

    @login_reqiure
    def post(self,request):
        res_msg={"status": False}
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            res_msg["status"] = True
            print(title,content)
        return HttpResponse(json.dumps(res_msg))


def get_user_obj(request):
    username = request.COOKIES.get("username")
    password = request.COOKIES.get("password")
    user = models.UserProfile.objects.filter(username=username, password=password).first()
    if not user:
        username = request.session.get("username")
        password = request.session.get("password")
        user = models.UserProfile.objects.filter(username=username, password=password).first()
    return user
