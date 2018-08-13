# this file will contain all the tests for linked.data.gov.au
import requests
import rdflib


# linked.data.gov.au/def/placenames
#
#   definitional resource, static hash URI ontology, therefore only a single RDF & HTML URI test
def def_placenames_rdf_1():
    # get the RDF version of the resource, using Content Negotiation
    r = requests.get('http://linked.data.gov.au/def/placenames', headers={'Accept': 'text/turtle'})

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by Content Negotiation does not have Content-Type set to text/turtle.'

    # check the result is parsable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode('utf-8'), format='turtle')
    except Exception as e:
        pass

    if g is None:
        raise AssertionError('RDF (turtle) result is not parsable')

    # check parsable RDF contains the correct title (label)
    q = '''
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title 
            WHERE {
                ?o  a owl:Ontology ;
                    rdfs:label ?title .
            }
        '''
    title = None
    for t in g.query(q):
        title = str(t['title']).strip()

    assert title == 'Place Names Ontology', \
        'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)'


def def_placenames_rdf_2():
    # get the RDF version of the resource, using Query String Arguments
    r = requests.get('http://linked.data.gov.au/def/placenames?_format=text/turtle')

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by _format Query String Argument does not have Content-Type set to text/turtle.'

    # check the result is parsable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode('utf-8'), format='turtle')
    except Exception as e:
        pass

    if g is None:
        raise AssertionError('RDF (turtle) result is not parsable')

    # check parsable RDF contains the correct title (label)
    q = '''
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title 
            WHERE {
                ?o  a owl:Ontology ;
                    rdfs:label ?title .
            }
        '''
    title = None
    for t in g.query(q):
        title = str(t['title']).strip()

    assert title == 'Place Names Ontology', \
        'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)'


def def_placenames_rdf_3():
    # get the RDF version of the resource, using file extension-like syntax
    r = requests.get('http://linked.data.gov.au/def/placenames.ttl')

    # check Content-Type
    assert 'text/turtle' in r.headers['Content-Type'], \
        'Response for RDF by file extension does not have Content-Type set to text/turtle.'

    # check the result is parsable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode('utf-8'), format='turtle')
    except Exception as e:
        pass

    if g is None:
        raise AssertionError('RDF (turtle) result is not parsable')

    # check parsable RDF contains the correct title (label)
    q = '''
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title 
            WHERE {
                ?o  a owl:Ontology ;
                    rdfs:label ?title .
            }
        '''
    title = None
    for t in g.query(q):
        title = str(t['title']).strip()

    assert title == 'Place Names Ontology', \
        'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)'


def def_placenames_html():
    # get the HTML version of the resource
    r = requests.get('http://linked.data.gov.au/def/placenames')

    # check Content-Type
    assert 'text/html' in r.headers['Content-Type'], \
        'Response for HTML does not have Content-Type set to text/html.'

    # check for HTML title ""
    assert '<title>Place Names Ontology</title>' \
           in r.content.decode('utf-8'), \
        'HTML response does not contain the correct <title> element.'


if __name__ == '__main__':
    def_placenames_rdf_1()
    def_placenames_rdf_2()
    def_placenames_rdf_3()
    def_placenames_html()
