
import os
import json
from pprint import pprint
from agldwg_ruleset import AGLDWG_ValidRuleSet


class TestAGLDWG_Ruleset:
    # marshalling function
    # add in array of results

    def __init__(self):
        self.result = []

        filename = 'test2.linked.data.gov.au.json'
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

        # load JSON file
        uris_object = None
        with open(file_path, 'r') as f:
            uris_object = json.load(f)

        # call the ruleset with the test info
        for key, val in uris_object.items():
            self.result.append(AGLDWG_ValidRuleSet(key, val))
            # break


if __name__ == '__main__':

    # Test driver
    test = TestAGLDWG_Ruleset()

    failed = False
    for result in test.result:
        if not result.passed:
            failed = True

    if not failed:
        print('All passed!')
    else:
        print('Test failed.')
        for reason in test.result:
            if len(reason.fail_reasons) is not 0:
                for fail in reason.fail_reasons:
                    pprint(fail)
                    print()
                # pprint(reason.fail_reasons)