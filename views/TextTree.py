import os

import django.db
import django.http

import xml.etree.ElementTree as ET

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
        keys = ('id', 'parent_id', 'reading', 'begin', 'end', 'contents')

        tree = {key: value for (key, value) in zip(keys, result)}
        tree['children'] = []

        parent_id = tree['parent_id']
        if parent_id is not None:

            trees[tree['parent_id']]['children'].append(tree)

        trees[tree['id']] = tree

    return trees

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

    return django.http.HttpResponse(string)

def TextTreeView(request, **kwargs):

    import django.template
    template = django.template.loader.get_template('orihime/text-tree.html')

    import django.shortcuts

    response = _TextTreeView(None, **kwargs).content.decode('utf-8')

    return django.shortcuts.render(request, 'orihime/text-tree.html', {"ANKI_Text": response, "toggle_snippet": ""})

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
