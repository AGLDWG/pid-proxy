class Rule:
    """
    Template for a Rule.

    This template class needs to be initialised with the standard Rule required parameters as well as any other
    instance parameters needed for the specific rule operation.

    It returns a standard rule return object which is a Python dict comprised of the Rule object's instance variables.
    """

    def __init__(self,
                 name,
                 definition,
                 authority,
                 passed,
                 fail_reasons,
                 components_total_count,
                 components_failed_count,
                 # components_failed -- night add this later
                 ):
        """
        Initialize the Rule object

        :param id: (string) the ID of the rule, assigned by the project this rule is for
        :param name: (string) the English version of the rule name
        :param definition: (string) the definition of the rule in words
        :param authority: (string) where the rule comes from
        :param passed (boolean)
        :param fail_reasons (list) a list of all the reasons the rule failed
        :param components_total_count (int) the number of things that could have failed
        :param components_failed_count (int) the number of things that did fail
        :return:
        """
        # set the static things
        self.id = Rule.make_id(name)
        self.name = name
        self.definition = definition
        self.authority = authority
        self.time = datetime.datetime.now()

        # set the dynamic things
        self.passed = passed
        self.fail_reasons = fail_reasons
        self.components_total_count = components_total_count
        self.components_failed_count = components_failed_count
        #self.components_failed = components_failed

    @staticmethod
    def make_id(name):
        # replace all nonASCII characters
        id = ''.join([i if ord(i) < 128 else '' for i in name])
        # replace spaces with underscores
        id = id.replace(' ', '_')
        id = id.lower()
        return id

class RuleSet:
    """
    Template for a RuleSet

    This template class needs to be initialised with the standard RuleSet required parameters as well as any other
    instance parameters needed for the specific Rule class instances that it contains to operate.

    It returns a standard ruleset return object which is a Python dict comprised of the RuleSet object's instance
    variables.
    """

    def __init__(self, name, rules, dependencies=None):
        """
        Initialise the RuleSet

        :param id: (string) ID of the RuleSet, allocated by the project
        :param name: (string) name of the RuleSet
        :return: (dict) ruleset return object
        """

        self.id = RuleSet.make_id(name)
        self.name = name
        self.time = datetime.datetime.now()
        self.passed = True  # if any of the Rules fail, so too does the RuleSet
        self.rules = rules
        self.fail_reasons = []
        for r in rules:
            assert isinstance(r, Rule), 'RuleSets\' rules must be Rules'
            if not r.passed:
                self.passed = False
                for fr in r.fail_reasons:
                    self.fail_reasons.append('Rule %s: %s' % (r.name, fr))

        # dependencies
        if dependencies is not None:
            assert isinstance(dependencies, list)
            for d in dependencies:
                assert isinstance(d, RuleSet), 'RuleSets\' dependencies must be other RuleSets'
            self.dependencies = dependencies

            # evaluate adherence to the dependencies
            for d in self.dependencies:
                if not d.passed:
                    self.passed = False

                    for fr in d.fail_reasons:
                        # this will compound the RuleSet name onto the Rule name and the fail reason
                        self.fail_reasons.append('RuleSet %s: %s' % (d.name, fr))

    @staticmethod
    def make_id(name):
        # replace all nonASCII characters
        id = ''.join([i if ord(i) < 128 else '' for i in name])
        # replace spaces with underscores
        id = id.replace(' ', '_')
        id = id.lower()
        return id




import requests
import rdflib
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import json

from pprint import pprint

class AGLDWG_ValidRuleSet(RuleSet):
    def __init__(self, uri, data):
        ruleset_id = uri
        ruleset_name = uri
        rules_results = []
        
        metadata = data['metadata']
        parameters_list = data['parameters']


        for parameters in parameters_list:
            ValidateRedirect(metadata, parameters)
            break

class ValidateRedirect(Rule):
    def __init__(self, metadata, parameters):
        self.id = metadata['id']
        self.name = metadata['name']
        self.definition = metadata['definition']
        self.authority = metadata['authority']
        self.passed = True
        self.fail_reasons = []
        self.components_total_count = 1
        self.components_failed_count = 0
        

        r = requests.get(parameters['from'], headers=parameters['headers'], allow_redirects=False, timeout=2)
        if(r.headers.get('Location') == parameters['to']):
            pass
        else:
            self.passed = False
            self.fail_reasons.append('For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(label, from_, to, str(r.headers.get('Location'))))
            self.components_failed_count = 1
        


# def validate_redirect(label, from_, to, headers=None):
#     r = requests.get(from_, headers=headers, allow_redirects=False, timeout=2)

#     assert r.headers.get('Location') == to, \
#         'For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(label, from_, to, str(r.headers.get('Location')))