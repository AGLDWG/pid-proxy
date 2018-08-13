# this file will contain all the tests for environment.data.gov.au
import requests


# environment.data.gov.au/def/ba/glossary*
#
#   definitional resource, hosted off site, test only for redirects
def def_ba_glossary():
    # get the RDF version of the resource, using Content Negotiation
    r = requests.get(
        'http://environment.data.gov.au/def/ba/glossary/aquifer',
        headers={'Accept': 'text/turtle'},
        allow_redirects=False
    )

    # check redirect location
    assert r.headers.get('Location') == 'http://registry2.it.csiro.au/def/ba/glossary/aquifer', \
        'The BA Glossary does not redirect to registry2.it.csiro.au'


def def_ba_glossary_html():
    # get the HTML version of the resource
    r = requests.get('http://environment.data.gov.au/def/ba/glossary/aquifer')

    # check Content-Type
    assert 'text/html' in r.headers['Content-Type'], \
        'Response for HTML does not have Content-Type set to text/html.'

    # check for HTML title ""
    assert '<title>The Australian Government Records Interoperability Framework (AGRIF) ontology</title>' \
           in r.content.decode('utf-8'), \
        'HTML response does not contain the correct <title> element.'


if __name__ == '__main__':
    def_ba_glossary()
