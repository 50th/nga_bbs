from django.views import View
from bbs_models import models
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.urls import resolve
import json


def login_reqiure(func):
    def inner(*args, **kwargs):
        request = args[1] if isinstance(args[0], View) else args[0]
        username = request.COOKIES.get("username")
        password = request.COOKIES.get("password")
        user_obj = models.UserProfile.objects.filter(username=username, password=password).first()
        if not user_obj:
            username = request.session.get("username")
            password = request.session.get("password")
            user_obj = models.UserProfile.objects.filter(username=username, password=password).first()
        if not user_obj:
            if not request.is_ajax():
                return redirect("bbs:login")
            else:
                url = reverse("bbs:login")
                res_msg = {"status": False, "code": 1, "msg": url}
                return HttpResponse(json.dumps(res_msg))
        request.session["username"] = user_obj.username
        request.session["password"] = user_obj.password
        rm = resolve(request.path)  # 获取ResolverMatch对象
        url_info = (rm.app_name + ":" + rm.url_name, request.method.lower())  # 获取url的别名和app_name
        permission_set = set()  # 获取该用户的所有权限
        for r in user_obj.roles.all():
            for p in r.permission.all():
                if p.action == 0:
                    permission_set.add((p.url_name, "get"))
                    permission_set.add((p.url_name, "post"))
                    permission_set.add((p.url_name, "put"))
                    permission_set.add((p.url_name, "delete"))
                else:
                    permission_set.add((p.url_name, p.get_action_display()))
        for p in user_obj.permissions.all():
            if p.action == 0:
                permission_set.add((p.url_name, "get"))
                permission_set.add((p.url_name, "post"))
                permission_set.add((p.url_name, "put"))
                permission_set.add((p.url_name, "delete"))
            else:
                permission_set.add((p.url_name, p.get_action_display()))
        if url_info not in permission_set:
            if not request.is_ajax():
                return render(request, "403.html")
            else:
                url = reverse("403")
                res_msg = {"status": False, "code": 1, "msg": url}
                return HttpResponse(json.dumps(res_msg))
        return func(*args, **kwargs)
    return inner


def permission_require(func):
    def inner(*args, **kwargs):
        request = args[1] if isinstance(args[0], View) else args[0]
        username = request.session.get("username")
        password = request.session.get("password")
        user_obj = models.UserProfile.objects.filter(username=username, password=password).first()
        rm = resolve(request.path)
        url_info = (rm.app_name + ":" + rm.url_name, request.method.lower())
        permission_set = set()
        for r in user_obj.roles.all():
            for p in r.permission.all():
                if p.action == 0:
                    permission_set.add((p.url_name, "get"))
                    permission_set.add((p.url_name, "post"))
                    permission_set.add((p.url_name, "put"))
                    permission_set.add((p.url_name, "delete"))
                else:
                    permission_set.add((p.url_name, p.get_action_display()))
        for p in user_obj.permissions.all():
            if p.action == 0:
                permission_set.add((p.url_name, "get"))
                permission_set.add((p.url_name, "post"))
                permission_set.add((p.url_name, "put"))
                permission_set.add((p.url_name, "delete"))
            else:
                permission_set.add((p.url_name, p.get_action_display()))
        print(permission_set)
        if url_info not in permission_set:
            if not request.is_ajax():
                return render(request, "403.html")
            else:
                url = reverse("403")
                res_msg = {"status": False, "code": 1, "msg": url}
                return HttpResponse(json.dumps(res_msg))
        return func(*args, **kwargs)
    return inner
