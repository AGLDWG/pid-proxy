import requests
import rdflib
import sys

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import json


def validate_redirect(json_file, label, from_, to, headers, case):
    r = requests.get(from_, headers=headers, allow_redirects=False, timeout=2)

    if r.headers.get("Location") == to:
        print("OK\n\n")
    else:
        if case.get("ignore_failure") is True:
            print("NOT OK, but ignoring failure")
            comment = case.get("comment")
            if comment is not None:
                print("comment: ", comment)
            print("\n")

        else:
            print("NOT OK\n\n")
            print("\n\nFor file '{}', test '{}',\n{} did not redirect to\n{}, instead\n{}".format(
                json_file, label, from_, to, str(r.headers.get("Location"))), file=sys.stderr)


def validate_all_redirects(json_file):
    print("validate_all_redirects for file: {}".format(json_file))
    uris = json.load(open(json_file, "r"))
    for uri, cases in uris.items():
        for case in cases:
            print("from: {}\nto: {}".format(case["from"], case["to"]))
            if len(case["headers"]) > 0:
                print("headers: {}".format(case["headers"]))
            validate_redirect(json_file, case["label"], case["from"], case["to"], case["headers"], case)
