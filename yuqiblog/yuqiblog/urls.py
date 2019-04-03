"""yuqiblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

# from django.conf.urls import urls
from django.contrib import admin
import posts.views
import sitepages.views
import accounts.views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls), ## make it secret
    path('home/', posts.views.home, name = "home"),
    path('posts/<int:pk>/', posts.views.post_details, name = "post_detail"),
    path('about/', sitepages.views.about, name="about"),

    path('signup/', accounts.views.signup, name='signup'),
    path('login/', accounts.views.loginview, name='login'),
    path('logout/', accounts.views.logoutview, name='logout'),
    path('create/', posts.views.create, name='create'), ### need more edit
    path('post/<int:pk>/comment/', posts.views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', posts.views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', posts.views.comment_remove, name='comment_remove'),
    #path('user/<username>', posts.views name='userposts')
    path('weather/', include('weather.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
