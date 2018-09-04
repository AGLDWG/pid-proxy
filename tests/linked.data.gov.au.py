# this file will contain all the tests for linked.data.gov.au

if __name__ == '__main__':
    import functions
    # functions.validate_all_redirects('linked.data.gov.au.json')
    functions.validate_turtle_response('http://linked.data.gov.au/def/placenames', 'Place Names Ontolodgy')