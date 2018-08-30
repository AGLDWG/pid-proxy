# this file will contain all the tests for linked.data.gov.au

if __name__ == '__main__':
    import functions
    functions.validate_all_redirects('linked.data.gov.au.json')

    # two test cases for validating rdf response
    functions.validate_turtle_response('http://linked.data.gov.au/def/placenames', 'Place Names Ontology')
    functions.validate_rdf_xml_response('https://gist.githubusercontent.com/edmondchuc/b9739f96a5d3868b4b72591a6abc7e15/raw/117bb25b6d42a92d82e54ca3f4885b1df1b1bcb9', 'pizza')