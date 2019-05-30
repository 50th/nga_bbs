from django.shortcuts import render, HttpResponse
from django import views
from bbs_models import models
import json


def index(request):
    user = models.UserProfile.objects.filter(username="root",password="1234").first()
    forum_count = models.Forum.objects.count()
    user_count = models.UserProfile.objects.count()
    topic_count = models.Topic.objects.count()
    permission_count = models.Permission.objects.count()
    rule_count = models.Rule.objects.count()
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
