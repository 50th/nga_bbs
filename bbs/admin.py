from django.contrib import admin
from bbs_models import models


admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Permission)

