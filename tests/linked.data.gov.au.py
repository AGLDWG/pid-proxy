# this file will contain all the tests for linked.data.gov.au
import requests
import rdflib
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import json


def validate_redirect(label, from_, to, headers=None):
    r = requests.get(from_, headers=headers, allow_redirects=False, timeout=2)

    assert r.headers.get('Location') == to, \
        'For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(label, from_, to, str(r.headers.get('Location')))


def test_html_response(uri, expected_title):
    # get the HTML version of the resource
    r = requests.get(uri)

    # check Content-Type
    assert 'text/html' in r.headers['Content-Type'], \
        'Response for HTML does not have Content-Type set to text/html.'

    # check for HTML title ""
    parsed_html = BeautifulSoup(r.content.decode('utf-8'), features="html.parser")
    received_title = parsed_html.head.find('title').text
    assert expected_title == received_title, \
        'HTML response does not contain the correct <title> element. Expected "{}" got "{}"'.format(expected_title, received_title)


# TODO: broaden this to RDF/XML as well as turtle
def test_turtle_response(uri, expected_title):
    # get the RDF version of the resource, using Content Negotiation
    r = requests.get(uri, headers={'Accept': 'text/turtle'})

    print(uri)
    print(r.headers)

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by Content Negotiation does not have Content-Type set to text/turtle.'

    # get the RDF version of the resource, using Query String Arguments
    r = requests.get(uri + '?_format=text/turtle')

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by _format Query String Argument does not have Content-Type set to text/turtle.'

    # get the RDF version of the resource, using file extension-like syntax
    r = requests.get(uri)

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by file extension does not have Content-Type set to text/turtle.'

    # check the result is parseable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode('utf-8'), format='turtle')
    except Exception as e:
        print(e)

    if g is None:
        raise AssertionError('RDF (turtle) result is not parsable')

    # check parsable RDF contains the correct title (label)
    q = '''
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?title 
            WHERE {{
                <{}>  a owl:Ontology .
                {{ ?o rdfs:label ?title . }}
                UNION
                {{ ?o skos:prefLabel ?title . }}
            }}
        '''.format(uri.replace('.ttl', ''))

    received_title = None
    for t in g.query(q):
        received_title = str(t['title']).strip()

    assert received_title == expected_title, \
        'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)'


def test_all_redirects():
    uris = json.load(open('linked.data.gov.au.json', 'r'))
    for uri, cases in uris.items():
        for case in cases:
            print('from: {}\nto: {}'.format(case['from'], case['to']))
            if len(case['headers']) > 0:
                print('headers: {}'.format(case['headers']))
            validate_redirect(case['label'], case['from'], case['to'], case['headers'])
            print('ok\n\n')


if __name__ == '__main__':
    # def_placenames_rdf_1()
    # def_placenames_rdf_2()
    # def_placenames_rdf_3()
    # def_placenames_html()



    #validate_html_response('http://linked.data.gov.au/def/reg-status', 'Registry Ontology\'s Status vocabulary')
    #validate_turtle_response('http://linked.data.gov.au/def/reg-status.ttl', 'Registry Ontology\'s Status vocabulary')


    test_all_redirects()
