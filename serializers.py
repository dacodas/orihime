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

class WordRelationSerializer(serializers.ModelSerializer):

    class Meta:

        model = WordRelation
        fields = ['text', 'word']

    serializers.SlugRelatedField(many=False,
                                 read_only=True,
                                 slug_field='text')
    serializers.SlugRelatedField(many=False,
                                 read_only=True,
                                 slug_field='word')

class SourceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Source
        fields = ['name']

class TextSerializer(serializers.ModelSerializer):

    source = serializers.SlugRelatedField(many=False,
                                          read_only=False,
                                          queryset=Source.objects.all(),
                                          slug_field='name')
    user = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=User.objects.all(),
                                        slug_field='email')
    # source = SourceSerializer

    class Meta:
        model = Text
        fields = ['contents', 'source', 'user']

# class WordSerializerPretty(serializers.ModelSerializer):

#     definition = serializers.SlugRelatedField(many=False,
#                                               read_only=True,
#                                               slug_field='contents')
#     user = serializers.SlugRelatedField(many=False,
#                                         read_only=False,
#                                         queryset=User.objects.all(),
#                                         slug_field='email')

#     class Meta:
#         model = Word
#         fields = ['reading', 'definition', 'user']

class WordSerializer(serializers.ModelSerializer):

    definition = serializers.SlugRelatedField(many=False,
                                              read_only=False,
                                              queryset=Text.objects.all(),
                                              slug_field='contents')
    user = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=User.objects.all(),
                                        slug_field='email')

    class Meta:
        model = Word
        fields = ['reading', 'definition', 'user']
