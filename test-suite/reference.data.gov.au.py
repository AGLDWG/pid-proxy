# this file contains all the tests for reference.data.gov.au
import requests
import rdflib


# reference.data.gov.au/def/ont/agrif
#
#   definitional resource, static hash URI ontology, therefore only a single RDF & HTML URI test
def def_ont_agrif_rdf_1():
    # get the RDF version of the resource, using Content Negotiation
    r = requests.get(
        "http://reference.data.gov.au/def/ont/agrif", headers={"Accept": "text/turtle"}
    )

    # check Content-Type
    assert (
        "text/turtle" in r.headers["Content-Type"]
    ), "Response for RDF by Content Negotiation does not have Content-Type set to text/turtle."

    # check the result is parsable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode("utf-8"), format="turtle")
    except Exception as e:
        pass

    if g is None:
        raise AssertionError("RDF (turtle) result is not parsable")

    # check parsable RDF contains the correct title (label)
    q = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title 
            WHERE {
                ?o  a owl:Ontology ;
                    rdfs:label ?title .
            }
        """
    title = None
    for t in g.query(q):
        title = str(t["title"]).strip()

    assert (
        title
        == "The Australian Government Records Interoperability Framework (AGRIF) ontology"
    ), "Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)"


def def_ont_agrif_rdf_2():
    # get the RDF version of the resource, using Query String Arguments
    r = requests.get("http://reference.data.gov.au/def/ont/agrif?_format=text/turtle")

    # check Content-Type
    assert (
        "text/turtle" in r.headers["Content-Type"]
    ), "Response for RDF by _format Query String Argument does not have Content-Type set to text/turtle."

    # check the result is parsable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode("utf-8"), format="turtle")
    except Exception as e:
        pass

    if g is None:
        raise AssertionError("RDF (turtle) result is not parsable")

    # check parsable RDF contains the correct title (label)
    q = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title 
            WHERE {
                ?o  a owl:Ontology ;
                    rdfs:label ?title .
            }
        """
    title = None
    for t in g.query(q):
        title = str(t["title"]).strip()

    assert (
        title
        == "The Australian Government Records Interoperability Framework (AGRIF) ontology"
    ), "Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)"


def def_ont_agrif_rdf_3():
    # get the RDF version of the resource, using file extension-like syntax
    r = requests.get("http://reference.data.gov.au/def/ont/agrif.ttl")

    # check Content-Type
    assert (
        "text/turtle" in r.headers["Content-Type"]
    ), "Response for RDF by file extension does not have Content-Type set to text/turtle."

    # check the result is parsable RDF
    g = None
    try:
        g = rdflib.Graph().parse(data=r.content.decode("utf-8"), format="turtle")
    except Exception as e:
        pass

    if g is None:
        raise AssertionError("RDF (turtle) result is not parsable")

    # check parsable RDF contains the correct title (label)
    q = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title 
            WHERE {
                ?o  a owl:Ontology ;
                    rdfs:label ?title .
            }
        """
    title = None
    for t in g.query(q):
        title = str(t["title"]).strip()

    assert (
        title
        == "The Australian Government Records Interoperability Framework (AGRIF) ontology"
    ), "Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .)"


def def_ont_agrif_html():
    # get the HTML version of the resource
    r = requests.get("http://reference.data.gov.au/def/ont/agrif")

    # check Content-Type
    assert (
        "text/html" in r.headers["Content-Type"]
    ), "Response for HTML does not have Content-Type set to text/html."

    # check for HTML title ""
    assert (
        "<title>The Australian Government Records Interoperability Framework (AGRIF) ontology</title>"
        in r.content.decode("utf-8")
    ), "HTML response does not contain the correct <title> element."


# TODO: implement custom tests for AGRIF demo (https://github.com/AGLDWG/agrif-demo)
def ont_agrif_demo_html():
    """Tests for the AGRIF demo
    """
    source = "http://reference.data.gov.au/agrifdemo"
    target = "http://www.linked.data.gov.au/reference.data.gov.au/agrifdemo"

    # get the HTML version of the demo
    r = requests.get(source, headers={"Accept": "text/html"}, allow_redirects=False)

    # check the redirection
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )

    # check for bad response code
    r.raise_for_status()


# reference.data.gov.au/def/ont/dataset
#
#   definitional resource, static hash URI ontology, therefore only a single RDF & HTML URI test
# TODO: copy AGRIF tests for dataset ont


# reference.data.gov.au/def/ont/iso19160-1-address
#
#   definitional resource, static hash URI ontology, therefore only a single RDF & HTML URI test
# TODO: copy AGRIF tests for dataset ont


# reference.data.gov.au/def/ont/iso19160-1-address-nz-profile
#
#   definitional resource, static hash URI ontology, therefore only a single RDF & HTML URI test
# TODO: copy AGRIF tests for dataset ont


if __name__ == "__main__":
    # def_ont_agrif_rdf_1()
    # def_ont_agrif_rdf_2()
    # def_ont_agrif_rdf_3()
    # def_ont_agrif_html()
    # ont_agrif_demo_html()
    #
    # print("All tests passed successfully!")

    import tests.functions as functions

    functions.validate_all_redirects("reference.data.gov.au.json")
