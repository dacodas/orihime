from django.contrib.auth.models import User, Group
from rest_framework import serializers

from orihime.models.monolith import Source, Text, Word, WordRelation

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class TextSerializer(serializers.ModelSerializer):

    source = serializers.SlugRelatedField(many=False,
                                          read_only=True,
                                          slug_field='name')
    user = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=User.objects.all(),
                                        slug_field='email')

    class Meta:
        model = Text
        fields = ['contents', 'source', 'user']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['name']
