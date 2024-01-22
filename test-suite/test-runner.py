# This is the test runner currently in use by the ARDC staging facility.

import glob

import tests.functions_keep_going as functions

if __name__ == "__main__":
    functions.validate_all_redirects("linked.data.gov.au.json")
    # All .json files in the linked.data.gov.au/org directory.
# Deliberate syntax error for test purposes. DO NOT MERGE!
    splat
    org_json = glob.glob('linked.data.gov.au/org/*.json')
    org_json.sort()
    for org in org_json:
        functions.validate_all_redirects(org)
