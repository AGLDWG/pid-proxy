# this file will contain all the tests for environment.data.gov.au
import requests
import inspect


# environment.data.gov.au/def/ba/glossary*
#
#   definitional resource, hosted off site, test only for redirects
def def_ba_glossary():
    # get the RDF version of the resource, using Content Negotiation
    r = requests.get(
        "http://environment.data.gov.au/def/ba/glossary/aquifer",
        headers={"Accept": "text/turtle"},
        allow_redirects=False,
    )

    # check redirect location
    assert (
        r.headers.get("Location")
        == "http://registry2.it.csiro.au/def/ba/glossary/aquifer"
    ), "The BA Glossary does not redirect to registry2.it.csiro.au"


def def_water_quality_op_rdf():
    """Water Quality Observable Properties Ontology  
    Test for redirection via URL redirect
    """
    source = "http://environment.data.gov.au/water/quality/def/op.rdf"
    target = "http://sissvoc.ereefs.info/repo/vocab/op.rdf"
    r = requests.get(
        source, headers={"Accept": "application/rdf+xml"}, allow_redirects=False
    )
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )


def def_water_quality_op_html():
    """Water Quality Observable Properties Ontology 
    Test for redirection via URL redirect
    """
    source = "http://environment.data.gov.au/water/quality/def/op.html"
    target = "http://sissvoc.ereefs.info/repo/vocab/op.html"
    r = requests.get(source, headers={"Accept": "text/html"}, allow_redirects=False)
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )


def def_water_quality_op_html_header():
    """Water Quality Observable Properties Ontology
    Test for redirection based on header content type
    """

    source = "http://environment.data.gov.au/water/quality/def/op"
    target = "http://sissvoc.ereefs.info/repo/vocab/op.html"
    r = requests.get(source, headers={"Accept": "text/html"}, allow_redirects=False)
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )


def def_water_quality_op_rdf_header():
    """Water Quality Observable Properties Ontology
    Test for redirection based on header content type
    """
    source = "http://environment.data.gov.au/water/quality/def/op"
    target = "http://sissvoc.ereefs.info/repo/vocab/op.rdf"
    r = requests.get(
        source, headers={"Accept": "application/rdf+xml"}, allow_redirects=False
    )
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )


def def_op_rdf_header():
    """eReefs legacy WQ def
    Test for redirection based on header content type
    """
    source = "http://environment.data.gov.au/def/op"
    target = "http://sissvoc.ereefs.info/repo/vocab/op.rdf"
    r = requests.get(
        source, headers={"Accept": "application/rdf+xml"}, allow_redirects=False
    )
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )


def def_op_html_header():
    """eReefs legacy WQ def
    Test for redirection based on header content type
    """
    source = "http://environment.data.gov.au/def/op"
    target = "http://sissvoc.ereefs.info/repo/vocab/op.html"
    r = requests.get(source, headers={"Accept": "text/html"}, allow_redirects=False)
    assert r.headers.get("Location") == target, (
        "Failed redirect from " + source + " to " + target
    )


if __name__ == "__main__":
    # def_ba_glossary()
    # def_water_quality_op_rdf()
    # def_water_quality_op_html()
    # def_water_quality_op_rdf_header()
    # def_water_quality_op_html_header()
    # def_op_rdf_header()
    # def_op_html_header()
    # print('All tests passed successfully!')

    import tests.functions as functions

    functions.validate_all_redirects("environment.data.gov.au.json")
