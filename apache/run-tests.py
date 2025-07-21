import httpx
import json
from pathlib import Path


def validate_redirect(json_file, label, from_, to, headers, case, server_root_url):
    from_ = str(from_).replace("https://linked.data.gov.au", server_root_url)
    r = httpx.get(from_, headers=headers, follow_redirects=False, timeout=10)

    if r.headers.get("Location") == to:
        print("OK\n\n")
        return True, None
    else:
        if case.get("ignore_failure") is True:
            print("NOT OK, but ignoring failure")
            comment = case.get("comment")
            if comment is not None:
                print("comment: ", comment)
            print("\n")
            return True, None
        else:
            print("NOT OK\n\n")
            return False, f"For file {json_file}, test {label},\n{from_} did not redirect to\n{to}, instead\n{r.headers.get('Location')}"


def validate_all_redirects(json_file, server_root_url):
    print("validate_all_redirects for file: {}".format(json_file))
    uris = json.load(open(json_file, "r"))
    errors = []
    for uri, cases in uris.items():
        for case in cases:
            print("from: {}\nto: {}".format(case["from"], case["to"]))
            if len(case["headers"]) > 0:
                print("headers: {}".format(case["headers"]))
            result, msg = validate_redirect(json_file, case["label"], case["from"], case["to"], case["headers"], case, server_root_url)
            if not result:
                errors.append(msg)

    print("\n")
    if len(errors) > 0:
        for msg in errors:
            print(msg)

        print(f"No. of errors: {len(errors)}")
    else:
        print("All tests passed")


if __name__ == "__main__":
    SERVER_ROOT_URL = "https://linked.data.gov.au/"

    TEST_SUITE_DIR = Path(__file__).parent.parent.resolve() / "test-suite"
    org_json = Path(TEST_SUITE_DIR / "linked.data.gov.au/org/").glob("*.json")

    for org in sorted(org_json):
        print(org.name)
        validate_all_redirects(org, SERVER_ROOT_URL)
