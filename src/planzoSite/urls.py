"""
URL configuration for planzoSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from base.views import home
from django.urls import path, include
from .views import loginView, signUpView, logoutUser, events, contact, petition_signup, about
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # path('events/', include('events')),
    # path('home/', home),
    

    # path('home/', home, name='home'),
    path('login/', loginView, name='login'),
    path('signup/',signUpView, name='signup'),
    path('accounts/login/', loginView, name='login'),
    path('accounts/signup/', signUpView, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', include('base.urls')), # added a base url
    path('home/', include('events.urls', namespace='events')),
    path('profiles/', include('profiles.urls', namespace='profiles')),

    # # User login & authentication views
    # path('login/', loginView, name='login'),
    # path('signup/', signUpView, name='signup'),
    # path('logout/', logoutUser, name='logout'),
    # path('about/', about, name='about'),
    # path('events/', events, name='events'),
    # path('contact/', contact, name='contact'),
    # path('petition_signup/', petition_signup, name='Petition'),

    # Admin routes(external packages access)
    path('accounts/login/', loginView, name='login'),
    path('accounts/signup/', signUpView, name='signup'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('events/', include('events.urls')),
]

# url patterns for events"
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)