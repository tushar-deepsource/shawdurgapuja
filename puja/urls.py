"""puja URL Configuration

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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, register_converter

from main import converters
from main.views import *

from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
url(r'^attachments/', include('attachments.urls', namespace='attachments')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('schedule/<yyyy:year>/',schedule,name="schedule"),

    url(r'^logout/$', user_logout, name='signout'),
   
    path('', home,name="Home"),
    path('videos/<yyyy:year>/<str:day>',video,name="Videos"),
    path('aboutyear/<yyyy:year>',about_year,name="About Year"),
    path('redirect/', redirect_view_puja,name="Redirect"),

    url(r'^filer/', include('filer.urls')),
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
