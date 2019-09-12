import logging
import requests
import django

import lxml.etree

import orihime.settings

@django.views.decorators.csrf.csrf_exempt
def search_goo(request, **kwargs):

    word = kwargs['word']
    response = requests.get(
        "{}/?reading={}".format(orihime.settings.GOO_LOCAL_HOST, word),
        headers={"Accept": "application/vnd+orihime.goo-results+html"})

    return HttpResponse(content = response.content)

@django.views.decorators.csrf.csrf_exempt
def search_larousse(request, **kwargs):
    
    word = kwargs['word']
    response = requests.get(
        "https://larousse.fr/dictionnaires/francais/{}"
        .format(word))

    root = lxml.etree.HTML(response.content)

    # This needs sanitization
    serialized_html = lxml.etree.tostring(root.xpath("//ul[@class='Definitions']")[0], encoding='utf-8').decode('utf-8')

    return HttpResponse(content = serialized_html)
