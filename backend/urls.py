"""nga_bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from backend import views

app_name = 'backend'
urlpatterns = [
    path('permission/', views.PermissionView.as_view(), name="permission"),
    path('role/', views.RoleView.as_view(), name="role"),
    path('forum/', views.ForumView.as_view(), name="forum"),
    re_path('forum/(?P<forum_id>\d+)/', views.ForumView.as_view(), name="forum"),
    path('', views.index, name="index"),
]
