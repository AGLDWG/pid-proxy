
import os
import json
from pprint import pprint
from agldwg_ruleset import AGLDWG_ValidRuleSet

class TestAGLDWG_Ruleset:
    def test(self):
        filename = 'test.linked.data.gov.au.json'
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

        uris_object = None
        with open(file_path, 'r') as f:
            uris_object = json.load(f)

        for key, val in uris_object.items():
            # pprint(key)
            # pprint(val)
            result = AGLDWG_ValidRuleSet(key, val)
            break
        # pprint(uris_object)

if __name__ == '__main__':

# Test driver
    test = TestAGLDWG_Ruleset().test()
    print('Finished!')