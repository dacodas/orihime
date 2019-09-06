from django.contrib.auth.models import User, Group
from rest_framework import serializers

from orihime.models import Source, Text, Word, WordRelation

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ['url', 'name']

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

class TextSerializer(serializers.ModelSerializer):

    source = serializers.SlugRelatedField(many=False,
                                          allow_null=True,
                                          read_only=False,
                                          queryset=Source.objects.all(),
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

class WordRelationSerializerCreateIntermediaries(serializers.ModelSerializer):

    definition = serializers.CharField()
    reading = serializers.CharField()
    user = serializers.SlugRelatedField(many=False,
                                        read_only=False,
                                        queryset=User.objects.all(),
                                        slug_field='email')

    class Meta:

        model = WordRelation
        fields = ['begin', 'end', 'definition', 'reading', 'user', 'text']

    def create(self, validated_data):

        definition_text = Text.objects.create(source=None,
                                              user=validated_data['user'],
                                              contents=validated_data['definition'])
        word = Word.objects.create(reading=validated_data['reading'],
                                   definition=definition_text,
                                   user=validated_data['user'])

        validated_data.pop('definition')
        validated_data.pop('reading')
        validated_data.pop('user')
        validated_data['word'] = word

        word_relation = super(WordRelationSerializerCreateIntermediaries, self).create(validated_data)

        return word_relation

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

