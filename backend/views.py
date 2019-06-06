from django.shortcuts import render, HttpResponse
from django import views
from bbs_models import models
import json


def index(request):
    user = models.UserProfile.objects.filter(username="root", password="1234").first()
    forum_count = models.Forum.objects.count()
    user_count = models.UserProfile.objects.count()
    topic_count = models.Topic.objects.count()
    permission_count = models.Permission.objects.count()
    role_count = models.Role.objects.count()
    return render(request, "backend/index.html", locals())


class ForumView(views.View):

    def get(self, request, *args, **kwargs):
        user = models.UserProfile.objects.filter(username="root", password="1234").first()
        forum_fields = tuple(models.Forum._meta.fields)
        forum_list = models.Forum.objects.values_list(*list(map(lambda v: v.name, forum_fields)))
        return render(request, "backend/show-forum.html", locals())

    def post(self, request):
        res_msg = {"status": True}
        name = request.POST.get("name")
        description = request.POST.get("description")
        forum = models.Forum.objects.filter(name=name).first()
        if forum:
            res_msg["status"] = False
            res_msg["msg"] = "板块已存在"
        else:
            forum = models.Forum.objects.create(name=name, description=description)
            forum.save()
        return HttpResponse(json.dumps(res_msg))


class PermissionView(views.View):
    def get(self, request):
        user = models.UserProfile.objects.filter(username="root", password="1234").first()
        permission_fields = tuple(models.Permission._meta.fields)
        permission_list = models.Permission.objects.values(*list(map(lambda v: v.name, permission_fields)))
        print(permission_list)
        action_choices = models.Permission.action_choices
        return render(request, "backend/show-permission.html", locals())

    def post(self,request):
        res_msg = {"status": True}
        name = request.POST.get("name")
        url_name = request.POST.get("urlName")
        action = int(request.POST.get("action"))
        permission_obj = models.Permission.objects.filter(url_name=url_name, action=action).first()
        if permission_obj:
            res_msg["status"] = False
            res_msg["msg"] = "权限已存在"
        else:
            permission_obj = models.Permission.objects.create(name=name, url_name=url_name, action=action)
            permission_obj.save()
        return HttpResponse(json.dumps(res_msg))


class RoleView(views.View):
    def get(self,request):
        user = models.UserProfile.objects.filter(username="root", password="1234").first()
        role_fields_temp = models.Role._meta.get_fields()
        role_fields = []
        for r in role_fields_temp:
            if isinstance(r, models.models.Field):
                role_fields.append(r)
        role_lsit = models.Role.objects.all()
        role_value_lsit = []
        for index, r in enumerate(role_lsit):
            print(index,r)
            role_value_lsit.append([])
            for f in role_fields:
                role_value_lsit[index].append(r.__getattribute__(f.name))
        print(role_value_lsit)
        permission_list = models.Permission.objects.all()
        return render(request, "backend\show-role.html", locals())

    def post(self, request):
        res_msg = {"status": True}
        role_data = json.loads(request.POST.get("roleData"))
        name = role_data.get("name")
        permission = role_data.get("permission")
        print(name, permission)
        if name and permission:
            role_obj = models.Role.objects.create(name=name)
            role_obj.save()
            role_obj.permission.add(*permission)
            role_obj.save()
        return HttpResponse(json.dumps(res_msg))
