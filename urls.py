from django.urls import path, include

from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views;
from django.contrib.flatpages import views
from django.conf import settings

import rest_framework.routers

import orihime.views 
import orihime.TinyMCEText

router = rest_framework.routers.SimpleRouter()
router.register(r'texts', orihime.views.ApiViews.TextViewSet)
router.register(r'words', orihime.views.ApiViews.WordViewSet)
router.register(r'sources', orihime.views.ApiViews.SourceViewSet)
router.register(r'word-relations', orihime.views.ApiViews.WordRelationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    # path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('tinymce/', include('tinymce.urls')),
    path('mce-test/', orihime.TinyMCEText.TinyMCETextView, name="tinymcetest"),

    path('text-tree/<int:id>', orihime.views.TextTree.TextTreeView, name="text-tree"),
    path('_text-tree/<int:id>', orihime.views.TextTree._TextTreeView, name="text-tree"),
    path('_word-relations/', orihime.views.WordRelationCreateWithIntermediaries.WordRelationCreateWithIntermediaries, name="_words-relations"),

    path('search/<str:word>', orihime.views.search.search_larousse, name="sources"),
    path('search/larousse/<str:word>', orihime.views.search.search_larousse, name="sources"),
    path('search/goo/<str:word>', orihime.views.search.search_goo, name="sources"),

    # oauth testing
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/hello', orihime.views.oauth.OauthApiEndpoint.as_view()),
]
