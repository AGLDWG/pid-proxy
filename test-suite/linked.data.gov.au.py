import tests.functions as functions
from pathlib import Path

if __name__ == "__main__":
    functions.validate_all_redirects(Path(__file__).parent / "linked.data.gov.au.json")
    # functions.validate_turtle_response('http://linked.data.gov.au/def/placenames', 'Place Names Ontolodgy')
    # functions.validate_turtle_response('http://reference.data.gov.au/def/ont/agrif', 'The Australian Government Records Interoperability Framework (AGRIF) ontology')
    # functions.validate_turtle_response('http://gnafld.net/def/gnaf', 'GNAF ontology')
    # functions.validate_turtle_response('https://gist.githubusercontent.com/edmondchuc/ea2cc0bb2ce8f0f2adfa583a34540153/raw/a53f3a550c96cba9098ef033aec001ac6511ee1b', 'pizza')
