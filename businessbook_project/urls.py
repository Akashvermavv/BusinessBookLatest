"""businessbook_project URL Configuration

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
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django_email_verification import urls as mail_urls
from . import views

urlpatterns = [
# 	path('',TemplateView.as_view(template_name='index.html'),name='index'),
    path('',views.home,name='index'),
    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    path('accounts/',include('accounts.urls')),
    path('campaign/',include('campaign.urls')),
    path('email/', include(mail_urls)),
    path('about-us/',TemplateView.as_view(template_name='about-us.html'),name='about-us'),
    path('support/',TemplateView.as_view(template_name='support.html'),name='support'),
    path('safety/',TemplateView.as_view(template_name='safety.html'),name='safety'),
    path('portfolio/',TemplateView.as_view(template_name='portfolio.html'),name='portfolio'),
    path('agent/',TemplateView.as_view(template_name='agent.html'),name='agent'),
    path('upcomming/',TemplateView.as_view(template_name='upcomming.html'),name='upcomming'),
     path('policy/',TemplateView.as_view(template_name='policy.html'),name='policy'),

      path('conditions/',TemplateView.as_view(template_name='terms.html'),name='conditions'),
    
   
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
