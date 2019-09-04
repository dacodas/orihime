from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseServerError

import xml.etree.ElementTree as ET

from rest_framework import viewsets, generics, permissions, decorators

from orihime.serializers import \
    UserSerializer, \
    GroupSerializer, \
    TextSerializer, \
    SourceSerializer, \
    WordRelationSerializer, \
    WordSerializer, \
    _WordRelationSerializer, \
    WordRelationSerializerCreateIntermediaries

from orihime.models.monolith import Source, Text, Word, WordRelation
from orihime.permissions import IsOwnerOrReadOnly

from oauth2_provider.views.generic import ProtectedResourceView

from lxml import etree

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
def search_goo(request, **kwargs):

    word = kwargs['word']
    response = requests.get(
        "http://localhost/blah.sum?reading={}".format(word),
        headers={"Accept": "application/vnd+orihime.goo-results+html"})

    return HttpResponse(content = response.content)

@django.views.decorators.csrf.csrf_exempt
def search_larousse(request, **kwargs):
    
    word = kwargs['word']
    response = requests.get(
        "https://larousse.fr/dictionnaires/francais/{}"
        .format(word))

    root = etree.HTML(response.content)

    # This needs sanitization
    serialized_html = etree.tostring(root.xpath("//ul[@class='Definitions']")[0], encoding='utf-8').decode('utf-8')

    return HttpResponse(content = serialized_html)

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

@decorators.api_view(['POST'])
def WordRelationCreateInt(request):

    import collections
    newQueryDict = request.data.copy()
    newQueryDict['user'] = request.user.email
    fauxRequest = collections.namedtuple('Request', 'data')(newQueryDict)

    word_relation_serializer = WordRelationSerializerCreateIntermediaries(data=fauxRequest.data)

    if not word_relation_serializer.is_valid():

        raise ValueError(word_relation_serializer.errors)

    word_relation = word_relation_serializer.create(word_relation_serializer.validated_data)
    
    return HttpResponse(content="You're gucci", content_type='text/plain', status=200)

class WordRelationCreate(UseCurrentUserMixin,
                         generics.CreateAPIView):

    serializer_class = WordRelationSerializerCreateIntermediaries
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    queryset = WordRelation.objects.all()

# Find out permissions, make sure users can only add relations between
# words and texts that they own
class WordRelationViewSet(viewsets.ModelViewSet):

    serializer_class = WordRelationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = WordRelation.objects.all()

# Find out permissions, make sure users can only add relations between
# words and texts that they own
class _WordRelationViewSet(viewsets.ModelViewSet):

    serializer_class = _WordRelationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = WordRelation.objects.all()

class SourceViewSet(viewsets.ModelViewSet):

    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Source.objects.all()

# https://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database


from django.db import connection

def sqlTextTree(id):

    # Instead of doing this, package the application, and use
    # distutils or setup packaging and source finding utilities
    import os
    sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "word-in-context.sql")

    with open(sql_file_path, "r") as f:

        query = f.read()

    with connection.cursor() as cursor:
        cursor.execute(query, [id])
        results = cursor.fetchall()

    return results

def TextTree(id):

    results = sqlTextTree(id)

    trees = dict()

    for result in results:
        keys = ('id', 'parent_id', 'reading', 'begin', 'end', 'contents')

        tree = {key: value for (key, value) in zip(keys, result)}
        tree['children'] = []

        parent_id = tree['parent_id']
        if parent_id is not None:

            trees[tree['parent_id']]['children'].append(tree)

        trees[tree['id']] = tree

    return trees

def renderDefinition(string, root):

    entities_text = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
    <!ENTITY nbsp ' '>
]>
'''

    string_sans_entities = string
    string = entities_text + string.replace('&#13;', '')

    # Will return either plain text or sanitized HTML
    try: 

        print("Parsing: \n{}".format(string))
        element = ET.fromstring(string)
        root.append(element)
 
    except ET.ParseError as e:
 
        print("Got parse error: {}".format(e))
        root.text = string_sans_entities

def addChildren(root, tree):

    words_list = ET.SubElement(root, 'ul', {'class': 'orihime-words'})

    for child in tree['children']:

        print("Adding child {} to {}".format(child['reading'], words_list))

        item = ET.SubElement(words_list, 'li', {'class': 'orihime-word'})
        ET.SubElement(item, 'div', {'class': 'reading'}).text = child['reading']
        definition = ET.SubElement(item, 'div', {'class': 'definition', 'id': str(child['id'])})

        renderDefinition(child['contents'], definition)

        addChildren(item, child)

def _TextTreeView(request, **kwargs):

    id = kwargs['id']

    trees = TextTree(id)

    root = ET.Element('div', {'id': 'orihime-text-tree'})
    definition = ET.SubElement(root, 'div', {'class': 'definition', 'id': str(id)})
    renderDefinition(trees[id]['contents'], definition)

    addChildren(root, trees[kwargs['id']])

    string = ET.tostring(root, method='html').decode('utf-8')
    print(string)

    return HttpResponse(string)

def TextTreeView(request, **kwargs):

    import django.template
    template = django.template.loader.get_template('text-tree.html')

    import django.shortcuts

    response = _TextTreeView(None, **kwargs).content.decode('utf-8')

    return django.shortcuts.render(request, 'text-tree.html', {"ANKI_Text": response, "toggle_snippet": ""})

class ApiEndpoint(ProtectedResourceView):

    def get(self, request, *args, **kwargs):

        return HttpResponse('Hello, OAuth2!')
