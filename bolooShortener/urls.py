"""
URL configuration for bolooShortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from shortener_app import views as shortener_views

urlpatterns = [
    path('', shortener_views.splash, name='splash'),
    path('admin/', admin.site.urls),
    path('home/', shortener_views.home, name='home'),
    path('login/', shortener_views.login, name='login'),
    path('logout/', shortener_views.logout, name='logout'),
    path('signup/', shortener_views.signup, name='signup'),
    path('shorten/', shortener_views.Shorten.as_view(), name='shorten'),
    path('manage/', shortener_views.manage, name='manage'),
    path('delete/', shortener_views.Delete.as_view(), name='delete'),
    path('<str:short_url>/', shortener_views.redirect_link, name='redirect'),
]
