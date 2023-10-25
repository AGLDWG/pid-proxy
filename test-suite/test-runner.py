import tests.functions_keep_going as functions

if __name__ == "__main__":
    functions.validate_all_redirects("linked.data.gov.au.json")
    functions.validate_all_redirects("linked.data.gov.au/org/abs.json")
    functions.validate_all_redirects("linked.data.gov.au/org/gsq.json")
    functions.validate_all_redirects("linked.data.gov.au/org/gswa.json")
    functions.validate_all_redirects("linked.data.gov.au/org/tern.json")
