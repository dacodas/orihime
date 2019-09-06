"""orihime URL Configuration

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
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views;
from django.urls import path, include

from orihime.views import \
    SourceViewSet, \
    TextViewSet, \
    WordRelationViewSet, \
    _WordRelationViewSet, \
    WordViewSet, \
    login_view, \
    search_larousse, \
    search_goo, \
    ApiEndpoint, \
    WordRelationSerializerCreateIntermediaries

from rest_framework import routers
from django.contrib.flatpages import views

import django.conf.urls.static
from django.conf import settings

import orihime
import orihime.mceflatpage.test

router = routers.SimpleRouter()
router.register(r'texts', TextViewSet)
router.register(r'word-relations', WordRelationViewSet)
# router.register(r'_word-relations', _WordRelationViewSet)
router.register(r'words', WordViewSet)
# router.register(r'_words', WordCreateTextView)
router.register(r'sources', SourceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/<str:word>', search_larousse, name="sources"),
    path('search/larousse/<str:word>', search_larousse, name="sources"),
    path('search/goo/<str:word>', search_goo, name="sources"),
    path('mce-test/', orihime.mceflatpage.test.mce_test, name="tinymcetest"),
    path('api/', include(router.urls)),
    path('text-tree/<int:id>', orihime.views.TextTreeView, name="text-tree"),
    path('_text-tree/<int:id>', orihime.views._TextTreeView, name="text-tree"),
    path('_word-relations/', orihime.views.WordRelationCreateInt, name="_words-relations"),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/hello', ApiEndpoint.as_view()),
    path('tinymce/', include('tinymce.urls')),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    # path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
] \
+ django.conf.urls.static.static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) \
+ router.urls
