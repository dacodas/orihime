from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseServerError

from rest_framework import viewsets, generics, permissions, decorators

from orihime.serializers import UserSerializer, GroupSerializer, TextSerializer, SourceSerializer, WordRelationSerializer, WordSerializer
from orihime.models.monolith import Source, Text, Word, WordRelation
from orihime.permissions import IsOwnerOrReadOnly

import requests
import django
import json
import rest_framework

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("<html><body>You're logged in! Love ya!</body></html>")
    else:
        return HttpResponse("<html><body>You're a piece of shit...</body></html>")

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
