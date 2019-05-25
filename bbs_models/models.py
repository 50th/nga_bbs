from django.db import models


class Permission(models.Model):
    """权限表"""
    name = models.CharField(max_length=32)
    action = models.CharField(max_length=32)

    def __str__(self):
        return self.per_name


class Rule(models.Model):
    """角色表"""
    name = models.CharField(max_length=32)
    permission = models.ManyToManyField("Permission", null=True)

    class Meta:
        db_table = "rule"

    def __str__(self):
        return self.rule_name


class UserProfile(models.Model):
    """用户表"""
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    registe_date = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField("Rule", null=True)
    permissions = models.ManyToManyField("Permission", null=True)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return self.user_name


class Forum(models.Model):
    """版块表"""
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)

    class Meta:
        db_table = "forum"

    def __str__(self):
        return self.name


class Topic(models.Model):
    """帖子表"""
    title = models.CharField(max_length=64)
    content = models.TextField()
    summary = models.CharField(max_length=64)
    image = models.ImageField(null=True)
    open_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("UserProfile", on_delete=models.DO_NOTHING)
    editor = models.ManyToManyField("UserProfile")

    class Meta:
        db_table = "topic"

    def __str__(self):
        return self.title
