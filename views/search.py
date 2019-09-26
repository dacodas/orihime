import logging
import requests
import django
import django.http
import bleach

import lxml.etree
import lxml.html

import orihime.settings

@django.views.decorators.csrf.csrf_exempt
def search_goo(request, **kwargs):

    word = kwargs['word']
    response = requests.get(
        "{}/?reading={}".format(orihime.settings.GOO_LOCAL_HOST, word),
        headers={"Accept": "application/vnd+orihime.goo-results+html"})

    return django.http.HttpResponse(content = response.content)

@django.views.decorators.csrf.csrf_exempt
def search_larousse(request, **kwargs):
    
    word = kwargs['word']
    response = requests.get(
        "https://larousse.fr/dictionnaires/francais/{}"
        .format(word))

    parsed_response = lxml.etree.HTML(response.content)
    first_definition = parsed_response.xpath("//ul[@class='Definitions']")[0]
    serialized_first_definition = lxml.etree.tostring(first_definition, encoding='utf-8').decode('utf-8')

    cleaner = orihime.OrihimeBleachCleaner.Cleaner()
    sanitized_definition = cleaner.clean(serialized_first_definition)

    parsed_sanitized_definition = lxml.html.fromstring(sanitized_definition)

    item = lxml.etree.Element('li')

    header = lxml.etree.Element('h1')
    header.text = word

    item.append(header)

    definition = lxml.etree.Element('div', {'class': 'definition'})
    definition.append(parsed_sanitized_definition)

    item.append(definition)

    serialized_item = lxml.etree.tostring(item, encoding='utf-8').decode('utf-8')

    return django.http.HttpResponse(content = serialized_item)
