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


def validate_html_response(uri, expected_title):
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


def is_rdf_parseable(r, expected_title, formatType):
    # check the result is parseable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode('utf-8'), format=formatType)
    except Exception as e:
        print(e)

    if g is None:
        raise AssertionError(f'RDF {formatType} result is not parsable')

    # define namespaces
    RDFS = rdflib.namespace.RDFS
    XSD = rdflib.namespace.XSD
    SKOS = rdflib.namespace.SKOS

    found_title = False
    # if not found_title:  # test for rdfs:label lang set to en on string literal
    #     for s, p, o in g.triples((None, RDFS.label, rdflib.term.Literal(expected_title, lang='en'))):
    #         found_title = True
    # if not found_title:  # test for rdfs:label lang set to none on string literal
    #     for s, p, o in g.triples((None, RDFS.label, rdflib.term.Literal(expected_title))):
    #         found_title = True
    # if not found_title:  # test for rdfs:label on xsd:string
    #     for s, p, o in g.triples((None, RDFS.label, rdflib.term.Literal(expected_title, datatype=XSD.string))):
    #         found_title = True
    # if not found_title:  # test for skos:label lang set to en on string literal
    #     for s, p, o in g.triples((None, SKOS.label, rdflib.term.Literal(expected_title, lang='en'))):
    #         found_title = True
    # if not found_title:  # test for skos:label lang set to none on string literal
    #     for s, p, o in g.triples((None, SKOS.label, rdflib.term.Literal(expected_title))):
    #         found_title = True
    # if not found_title:  # test for skos:label on xsd:string
    #     for s, p, o in g.triples((None, SKOS.label, rdflib.term.Literal(expected_title, datatype=XSD.string))):
    #         found_title = True
    # if not found_title:  # test for skos:prefLabel lang set to en on string literal
    #     for s, p, o in g.triples((None, SKOS.prefLabel, rdflib.term.Literal(expected_title, lang='en'))):
    #         found_title = True
    # if not found_title:  # test for skos:prefLabel lang set to none on string literal
    #     for s, p, o in g.triples((None, SKOS.prefLabel, rdflib.term.Literal(expected_title))):
    #         found_title = True
    # if not found_title:  # test for skos:label on xsd:string
    #     for s, p, o in g.triples((None, SKOS.prefLabel, rdflib.term.Literal(expected_title, datatype=XSD.string))):
            found_title = True
    
    # test to get title string
    for s, p, o in g.triples((None, RDFS.label, None)):
        if o == expected_title:
            found_title = True
        print(f'Title name found as: {o}')

    assert found_title == True, \
        'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .) or the expected title did not match.'

    return found_title


def validate_rdf_xml_response(uri, expected_title):
    # get the RDF version of the resource, using Content Negotiation
    r = requests.get(uri, headers={'Accept': 'application/rdf+xml'})

    print(uri)
    print(r.headers)

    # check Content-Type
    assert 'application/rdf+xml' in r.headers['Content-Type'], \
        'Response for RDF by Content Negotiation does not have Content-Type set to application/rdf+xml.'

    # get the RDF version of the resource, using Query String Arguments
    r = requests.get(uri + '?_format=application/rdf+xml')

    # check Content-Type
    assert 'application/rdf+xml' in r.headers['Content-Type'], \
        'Response for RDF by _format Query String Argument does not have Content-Type set to application/rdf+xml.'

    # get the RDF version of the resource, using file extension-like syntax
    r = requests.get(uri + '.rdf')

    # check Content-Type
    assert 'application/rdf+xml' in r.headers['Content-Type'], \
        'Response for RDF by file extension does not have Content-Type set to application/rdf+xml.'

    result = is_rdf_parseable(r, expected_title, 'application/rdf+xml')
    print(f'Title found: {result}')

# TODO: broaden this to RDF/XML as well as turtle
def validate_turtle_response(uri, expected_title):
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
    r = requests.get(uri  + '.ttl')

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by file extension does not have Content-Type set to text/turtle.'

    result = is_rdf_parseable(r, expected_title, 'text/turtle')
    print(f'Title found: {result}')

    # # check parsable RDF contains the correct title (label)
    # q = '''
    #         PREFIX owl: <http://www.w3.org/2002/07/owl#>
    #         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #         PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    #         SELECT ?title
    #         WHERE {{
    #             <{}>  a owl:Ontology .
    #             {{ ?o rdfs:label ?title . }}
    #             UNION
    #             {{ ?o skos:prefLabel ?title . }}
    #         }}
    #     '''.format(uri.replace('.ttl', ''))
    #
    # received_title = None
    # print("start")
    # for t in g.query(q):
    #     print(f'test value: {t}')
    #     received_title = str(t['title']).strip()
    #     if (received_title != None):
    #         break
    #
    # assert received_title == expected_title, \
    #     'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)'


def validate_all_redirects(json_file):
    uris = json.load(open(json_file, 'r'))
    for uri, cases in uris.items():
        for case in cases:
            print('from: {}\nto: {}'.format(case['from'], case['to']))
            if len(case['headers']) > 0:
                print('headers: {}'.format(case['headers']))
            validate_redirect(case['label'], case['from'], case['to'], case['headers'])
            print('ok\n\n')
