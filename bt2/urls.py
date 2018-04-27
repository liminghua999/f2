"""bt2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.generic import RedirectView
from django.contrib import admin
from hostinfo import urls as hostinfourls
from VersionIterration import urls as versionurls
from login import views as lviews
from login import yanzhengma

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hostinfo/',include(hostinfourls)),
    url(r'^$',lviews.Login,name='login'),
    url(r'^lgout/$',lviews.LoginOut,name="lgout"),
    url(r'^lgecode/$',lviews.send_msg,name="sendecode"),
    url(r'^checkcode/$',yanzhengma.check_code,name="check_code"),
    url(r'^version/',include(versionurls)),
]
