import logging
import requests
import django
import json
import rest_framework

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseServerError

from rest_framework import viewsets, permissions

from orihime.serializers import \
    UserSerializer, \
    GroupSerializer, \
    TextSerializer, \
    SourceSerializer, \
    WordRelationSerializer, \
    WordSerializer, \
    _WordRelationSerializer, \
    WordRelationSerializerCreateIntermediaries

from orihime.models import Source, Text, Word, WordRelation
from orihime.permissions import IsOwnerOrReadOnly

from . import mixins

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TextViewSet(mixins.UseCurrentUserMixin,
                  viewsets.ModelViewSet):

    serializer_class = TextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    queryset = Text.objects.all()

class WordViewSet(mixins.UseCurrentUserMixin,
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

# Find out permissions, make sure users can only add relations between
# words and texts that they own
class _WordRelationViewSet(viewsets.ModelViewSet):

    serializer_class = _WordRelationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = WordRelation.objects.all()

