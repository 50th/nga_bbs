from django.db import models


class Permission(models.Model):
    """权限表"""
    name = models.CharField(max_length=32, unique=False)
    url_name = models.CharField(max_length=64)
    action_choices = (
        (0, "all"),
        (1, "get"),
        (2, "post"),
        (3, "put"),
        (4, "delete"),
    )
    action = models.IntegerField(choices=action_choices, default=0)

    class Meta:
        db_table = "permission"
        unique_together = ("url_name", "action")

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32)
    permission = models.ManyToManyField("Permission")

    class Meta:
        db_table = "role"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """用户表"""
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=16, null=True, blank=True)
    id_card = models.CharField(max_length=18, null=True, blank=True)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.IntegerField(null=True, blank=True)
    # avatar = models.ImageField(width_field=50)
    register_date = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField("Role", blank=True)
    permissions = models.ManyToManyField("Permission", blank=True)
    avatar = models.ImageField(default="/static/image/avatar/default.gif")
    status_choices = (
        (0, "未激活"),
        (1, "正常"),
        (2, "警告"),
        (3, "nuke"),
    )
    status = models.IntegerField(choices=status_choices, default=0)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return self.username


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
    image = models.ImageField(null=True, blank=True)
    open_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("UserProfile", related_name="open_user", on_delete=models.DO_NOTHING)
    forum = models.ForeignKey("Forum", on_delete=models.DO_NOTHING, default=1)
    floor_count = models.IntegerField(default=0)
    editor = models.ManyToManyField("UserProfile", related_name="editor", blank=True)

    class Meta:
        db_table = "topic"

    def __str__(self):
        return self.title


class Like(models.Model):
    """点赞"""
    topic = models.ManyToManyField("Topic")
    from_user = models.ManyToManyField("UserProfile")

    class Meta:
        db_table = "like"

    def __str__(self):
        return "%s like %s" % (self.from_user, self.topic)


class Comment(models.Model):
    """评论"""
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    parent_comment = models.OneToOneField("Comment", on_delete=models.DO_NOTHING, null=True, blank=True)
    content = models.TextField()
    from_user = models.ForeignKey("UserProfile", on_delete=models.DO_NOTHING)
    floor = models.IntegerField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.from_user
