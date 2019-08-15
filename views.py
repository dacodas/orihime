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

# Find out permissions, make sure users can only add relations between
# words and texts that they own
class WordRelationViewSet(viewsets.ModelViewSet):

    serializer_class = WordRelationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = WordRelation.objects.all()

class SourceViewSet(viewsets.ModelViewSet):

    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Source.objects.all()

# https://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database


from django.db import connection

def TextTreeView(text_id):

    # Instead of doing this, package the application, and use
    # distutils or setup packaging and source finding utilities
    import os
    sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "word-in-context.sql")

    with open(sql_file_path, "r") as f:

        query = f.read()

    with connection.cursor() as cursor:
        cursor.execute(query, [text_id])
        results = cursor.fetchall()

    trees = dict()

    for result in results:
        keys = ('id', 'parent_id', 'reading', 'begin', 'end', 'contents')

        tree = {key: value for (key, value) in zip(keys, result)}
        tree['children'] = []

        parent_id = tree['parent_id']
        if parent_id is not None:

            trees[tree['parent_id']]['children'].append(tree)

        trees[tree['id']] = tree

    import xml.etree.ElementTree as ET

    root = ET.Element('div')
    ET.SubElement(root, 'p').text = trees[1]['contents']

    def addChildren(root, tree):

        mylist = ET.SubElement(root, 'ul')

        for child in tree['children']:

            item = ET.SubElement(mylist, 'li')
            item.text = child['reading']
            new_root = ET.SubElement(item, 'div')
            ET.SubElement(new_root, 'p').text = child['contents']
            addChildren(new_root, child)

    addChildren(root, trees[1])

    return ET.ElementTree(root)
