"""relicmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from app1 import urls
from app1 import views
import app1.urls
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('admin/', login_required(admin.site.urls)),
    path('user_list/', login_required(views.user_list)),
    path('relic_list/', login_required(views.relic_list)),
    path('photo_list/', login_required(views.photo_list)),
    path('video_list/', login_required(views.video_list)),

    path('add_user/', login_required(views.add_user)),
    path('delete_user/', login_required(views.delete_user)),
    path('remark_user/', login_required(views.remark_user)),
    path('upload_user/', login_required(views.upload_user)),

    path('add_relic/', login_required(views.add_relic)),
    path('delete_relic/', login_required(views.delete_relic)),

    path('upload_photo/', login_required(views.upload_photo)),
    path('upload_video/', login_required(views.upload_video)),

    path('data_analyse/', login_required(views.data_analyse)),

    path('regist/', views.regist),
    path('login/', views.login),
    path('logout/', views.logout),

    path('index/', views.login),
    path('admin/', admin.site.urls),

    # path('test/', views.test),

    # path('', include(app1.urls)),
    # path('', TemplateView.as_view(template_name="index.html")),
    path('', views.login),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
