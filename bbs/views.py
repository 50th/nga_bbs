from django.shortcuts import render, HttpResponse, redirect, reverse
from bbs_models import models
import json
from common import valid_code


def index(request):
    return render(request, "index.html")


def user_login(request):
    next_page = request.GET.get("next")
    if not next_page:
        next_page = reverse("index")
    if request.method == "POST":
        username_type = request.POST.get("type")
        username = request.POST.get("username")
        password = request.POST.get("password")
        code = request.POST.get("validCode")
        keep_login = request.POST.get("keepLogin")
        login_msg = {}
        if code == request.session["valid_code"]:
            if username_type == "email":
                user = models.UserProfile.objects.filter(email=username, password=password).first()
            elif username_type == "mobail":
                user = models.UserProfile.objects.filter(phone=username, password=password).first()
            else:
                user = models.UserProfile.objects.filter(username=username, password=password).first()
            if user:
                request.session["username"] = user.username
                request.session["password"] = user.password
                login_msg["status"] = True
                login_msg["msg"] = "ok"
                login_msg["next"] = next_page
                ht = HttpResponse(json.dumps(login_msg))
                if keep_login == "true":
                    ht.cookies["username"] = user.username
                    ht.cookies["password"] = user.password
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
        username = request.COOKIES.get("username")
        password = request.COOKIES.get("password")
        user = models.UserProfile.objects.filter(username=username, password=password).first()
        if not user:
            username = request.session.get("username")
            password = request.session.get("password")
            user = models.UserProfile.objects.filter(username=username, password=password).first()
        if user:
            return redirect("index")
        return render(request, "bbs/account_login.html", {"next_page": next_page})


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
