
import os
import json
from pprint import pprint
from agldwg_ruleset import AGLDWG_ValidRuleSet

# marshalling function
# add in array of results
class TestAGLDWG_Ruleset:

    def __init__(self):
        self.result = None

        filename = 'test.linked.data.gov.au.json'
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

        uris_object = None
        with open(file_path, 'r') as f:
            uris_object = json.load(f)

        for key, val in uris_object.items():
            # pprint(key)
            # pprint(val)
            self.result = AGLDWG_ValidRuleSet(key, val)
            
            # break
        # pprint(uris_object)

if __name__ == '__main__':

    # Test driver
    test = TestAGLDWG_Ruleset()

    
    if test.result.passed:
        print('All passed!')
    else:
        print('Test failed.')
        print(test.result.fail_reasons)