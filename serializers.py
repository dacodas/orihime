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

# Same as below, but specify text with an ID
class _WordRelationSerializer(serializers.ModelSerializer):

    text = serializers.PrimaryKeyRelatedField(many=False,
                                              read_only=False,
                                              queryset=Text.objects.all())
    word = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=Word.objects.all(),
                                        slug_field='reading')

    class Meta:

        model = WordRelation
        fields = ['text', 'word', 'begin', 'end']

class WordRelationSerializer(serializers.ModelSerializer):

    text = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=Text.objects.all(),
                                        slug_field='contents')
    word = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=Word.objects.all(),
                                        slug_field='reading')

    class Meta:

        model = WordRelation
        fields = ['text', 'word', 'begin', 'end']


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
