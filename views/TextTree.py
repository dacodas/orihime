import os

import django.db
import django.http
import django.template
import django.shortcuts

from django.utils.translation import gettext, gettext_lazy

import lxml.html

import bleach

import logging

import orihime.OrihimeBleachCleaner

logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database
def sqlTextTree(id):

    # Instead of doing this, package the application, and use
    # distutils or setup packaging and source finding utilities
    sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "word-in-context.sql")

    with open(sql_file_path, "r") as f:

        query = f.read()

    with django.db.connection.cursor() as cursor:
        cursor.execute(query, [id])
        results = cursor.fetchall()

    return results

def TextTree(id):

    results = sqlTextTree(id)

    trees = dict()

    for result in results:

        keys = ('ParentTextID', 'ChildTextID', 'ChildWordID', 'reading', 'SourceID', 'SourceName', 'begin', 'end', 'contents')
        # keys = ('id'', 'parent_id', 'reading', 'begin', 'end', 'contents')

        tree = {key: value for (key, value) in zip(keys, result)}
        tree['children'] = []

        parent_id = tree['ParentTextID']
        if parent_id is not None:

            trees[parent_id]['children'].append(tree)

        childTextID = tree['ChildTextID']
        trees[childTextID] = tree

    return trees

def addChildren(root, tree):

    words_list = lxml.html.Element('ul', {'class': 'orihime-words'})
    root.append(words_list)

    for child in tree['children']:

        logger.debug("Adding child {} to {}".format(child['reading'], words_list))

        item = lxml.html.Element('li', {'class': 'orihime-word', 'id': str(child['ChildWordID'])})
        words_list.append(item)

        reading = lxml.html.Element('div', {'class': 'reading'})
        reading.text = child['reading']
        item.append(reading)

        definition = lxml.html.Element('div', {'class': 'definition', 'id': str(child['ChildTextID'])})
        item.append(definition)

        renderDefinition(child['contents'], definition)
        renderSource(definition, child)

        addChildren(item, child)

# This endpoint is used in the Javascript
def _TextTreeView(request, **kwargs):

    id = kwargs['id']
    trees = TextTree(id)

    root = lxml.html.Element('div', {'id': 'orihime-text-tree'})
    definition = lxml.html.Element('div', {'class': 'definition', 'id': str(id)})
    root.append(definition)

    renderDefinition(trees[id]['contents'], definition)
    renderSource(definition, trees[id])

    addChildren(root, trees[id])

    string = lxml.html.tostring(root).decode('utf-8')
    logger.debug(string)

    return django.http.HttpResponse(string)

def TextTreeView(request, **kwargs):

    text_tree = _TextTreeView(request, **kwargs).content.decode('utf-8')

    return django.shortcuts.render(request, 'orihime/text-tree.html', {"text_tree": text_tree})

def renderSource(root, source):

    source_element = lxml.html.Element('span', {'class': 'source', 'id': str(source['SourceID'])})
    source_element.text = "{}: {}".format(gettext("Source"), source['SourceName'])
    root.append(source_element)

def renderDefinition(string, root):
    """
    # The below is no longer a concern... We are now using lxml
    # instead of html5lib
    # 
    # There are different ways we can parse this string using
    # html5lib.parse. I've elected to go with the default etree
    # implementation as

    # 1. It is the default
    # 2. The rest of the tree code is already using etree

    # The etree implementation appears to use SAX instead of DOM to
    # process the XML which means it can be online, rather than having
    # to process the entire document before exposing it to the user.
    # This is nice, but doesn't have all the bells and whistles of DOM.
    
    TODO: Let's think about stripping out tags we don't want...
    TODO: Let's initialize this custom sanitizer elsewhere in a module
    TODO: Consider using namespaces for each of the backend to allow
    easier styling. Classes might also work, but this would be a good
    test case
"""

    cleaner = orihime.OrihimeBleachCleaner.Cleaner()
    clean_string = cleaner.clean(string)

    parsed_div = lxml.html.fromstring(clean_string)
    root.append(parsed_div)
