import collections
import logging
import django.http

import rest_framework.decorators

from orihime.serializers import WordRelationSerializerCreateIntermediaries

logger = logging.getLogger()

@rest_framework.decorators.api_view(['POST'])
def WordRelationCreateWithIntermediaries(request):

    newQueryDict = request.data.copy()
    newQueryDict['user'] = request.user.email
    fauxRequest = collections.namedtuple('Request', 'data')(newQueryDict)

    logger.debug(request.user)
    logger.debug(request.user.email)
    logger.debug(request.user.is_authenticated)

    word_relation_serializer = WordRelationSerializerCreateIntermediaries(data=fauxRequest.data)

    if not word_relation_serializer.is_valid():

        raise ValueError(word_relation_serializer.errors)

    word_relation = word_relation_serializer.create(word_relation_serializer.validated_data)
    
    return django.http.HttpResponse(content="You're gucci", content_type='text/plain', status=200)
