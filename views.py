from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseServerError

from rest_framework import viewsets, generics, permissions, decorators

import rest_framework

from orihime.serializers import UserSerializer, GroupSerializer, TextSerializer, SourceSerializer, WordRelationSerializer, WordSerializer
from orihime.models.monolith import Source, Text, Word, WordRelation
from orihime.permissions import IsOwnerOrReadOnly

import requests

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("<html><body>You're logged in! Love ya!</body></html>")
    else:
        return HttpResponse("<html><body>You're a piece of shit...</body></html>")

def add_text():

    pass

def show_text():

    pass

def add_child_word_to_text():

    pass

import django
import json
@django.views.decorators.csrf.csrf_exempt
def search(request):

    ORIHIME_SEARCH = object()
    ORIHIME_SEARCH_URI = "http://localhost:8081/search"
    # 45.79.93.109

    print(request.POST)
    print(request.content_params)

    params = {x: request.POST[x] for x in ['backend', 'reading']}

    response = requests.post(ORIHIME_SEARCH_URI, params=params)

    if response.status_code != 200:

        return HttpResponseServerError(content="That's our bad... Orihime search failed!", reason="Orihime search failed")

    else:
        
        return HttpResponse(content=response.content, content_type='text/plain', status=200)

class UseCurrentUserMixin():

    # Or restrict by this... Or can that just be handled with permissions_clases?
    # def get_queryset(self):
    #     return self.request.user.accounts.all()
    def create(self, request, *args, **kwargs):

        import collections
        newQueryDict = request.data.copy()
        newQueryDict['user'] = request.user.email
        fauxRequest = collections.namedtuple('Request', 'data')(newQueryDict)

        return super(UseCurrentUserMixin, self).create(fauxRequest, *args, **kwargs)

class TextViewSet(UseCurrentUserMixin,
                  viewsets.ModelViewSet):

    serializer_class = TextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    queryset = Text.objects.all()

# class WordViewSet(UseCurrentUserMixin,
#                   viewsets.mixins.CreateModelMixin,
#                   viewsets.mixins.UpdateModelMixin,
#                   viewsets.mixins.DestroyModelMixin,
#                   viewsets.GenericViewSet):

#     # Same as ModelViewSet, but for retrieve and list serialize in a
#     # pretty way

#     serializer_class = WordSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]

#     queryset = Word.objects.all()

#     def _get_pretty_serializer(self, *args, **kwargs):

#         serializer_class = WordSerializerPretty
#         kwargs['context'] = self.get_serializer_context()
#         return serializer_class(*args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self._get_pretty_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self._get_pretty_serializer(queryset, many=True)
#         return rest_framework.response.Response(serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self._get_pretty_serializer(instance)
#         return rest_framework.response.Response(serializer.data)

class WordViewSet(UseCurrentUserMixin,
                  viewsets.ModelViewSet):

    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    queryset = Word.objects.all()

class WordRelationViewSet(UseCurrentUserMixin,
                          viewsets.ModelViewSet):

    serializer_class = WordRelationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    queryset = WordRelation.objects.all()

class SourceViewSet(viewsets.ModelViewSet):

    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Source.objects.all()

# https://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database

# class WordRelationList(generics.ListCreateAPIView):

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]

#     queryset = WordRelation.objects.all()
#     serializer_class = WordRelationSerializer
