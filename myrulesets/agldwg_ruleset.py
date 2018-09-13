import datetime

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


class RuleInheritanceError(Exception):
    """This Ruleset's exception class.
    
    Arguments:
        Exception {string} -- The error message that caused the exception.
    """
    pass


class AGLDWG_ValidRuleSet(RuleSet):
    def __init__(self, uri, data):
        ruleset_name = uri
        rules_results = []
        metadata = None
        components = None

        # check that metadata key exists
        test = ValidateMetadataIsPresent(uri, data)
        rules_results.append(test)
        if test.passed:
            metadata = data['metadata']
            components = data['components']
            # test for valid metadata
            test = ValidateMetadata(uri, metadata)
            rules_results.append(test)

        if test.passed:
            for component in components:
                # validate the components
                test = ValidateComponent(uri, component)
                rules_results.append(test)
                if not test.passed:
                    break

                # test each rule
                failed = False # if any of the rules fail, then stop
                for rule in component['rules']:
                    if rule == 'html':
                        test = ValidateHTML(uri, metadata, component)
                        rules_results.append(test)

                    if rule == 'rdf':
                        test = ValidateRDF(uri, metadata, component)
                        rules_results.append(test)
                #     if rule == 'html':
                #         # test = ValidateRedirect(metadata, component)
                #         test = ValidateHTML()
                #         rules_results.append(test)

                    # if rule == 'html_title':
                    #     test = ValidateHTMLResponse(uri, metadata, component)
                    #     rules_results.append(test)
                    #
                    # if rule == 'rdf':
                    #     test = ValidateTurtleResponse('hello', metadata, component)
                    #
                    # # if any tests failed, stop
                    # if not test.passed:
                    #     failed = True
                    #     break


                # if failed: # if a component fails, stop
                #     break

        RuleSet.__init__(self, ruleset_name, rules_results)



class ValidateRDF(Rule):
    def __init__(self, uri:str, metadata:dict, component:list):
        passed = True
        fail_reasons = []
        total_components = 1 #TODO:

        ### turtle file-extension-like
        _from = component['from'] + '.ttl'
        _to = component['to'] + '.ttl'
        _headers = {}  # {"Accept": "text/turtle"}

        # check the redirect for turtle
        r = requests.get(_from, _headers, allow_redirects=False, timeout=2)
        if (r.headers.get('Location') == _to):
            # check that the content type is set correctly
            if r.headers['Content-Type'] is not 'text/turtle':
                passed = False
                fail_reasons.append(f'{_from} Response for turtle by file extension does not have Content-Type set to text/turtle')
            else:
                # check that the RDF is parsable and that it contains the expected title
                result = self.is_rdf_parsable(self, r, uri, component['title'], 'text/turtle')
                if not result['titleFound']:
                    passed = False
                    theFoundTitle = result['title']
                    fail_reasons.append(f'{_from} RDF title found as \'{theFoundTitle}\'' + result['message'])
        else:
            passed = False
            fail_reasons.append(
                'For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(component['label'],
                                                                                                 _from,
                                                                                                 _to, str(
                        r.headers.get('Location'))))

        ### END of turtle file-extension-like

        ### turtle QSA
        _from = component['from'] + '?_format=text/turtle'

        # check the redirect for turtle
        r = requests.get(_from, _headers, allow_redirects=False, timeout=2)
        if (r.headers.get('Location') == _to):
            # check that the content type is set correctly
            if r.headers['Content-Type'] is not 'text/turtle':
                passed = False
                fail_reasons.append(f'{_from} Response for turtle by QSA does not have Content-Type set to text/turtle')
            else:
                # check that the RDF is parsable and that it contains the expected title
                result = self.is_rdf_parsable(self, r, uri, component['title'], 'text/turtle')
                if not result['titleFound']:
                    passed = False
                    theFoundTitle = result['title']
                    fail_reasons.append(f'{_from} RDF title found as \'{theFoundTitle}\'' + result['message'])
        else:
            passed = False
            fail_reasons.append(
                'For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(component['label'],
                                                                                                 _from,
                                                                                                 _to, str(
                        r.headers.get('Location'))))
        ### END of turtle QSA

        ### turtle conneg
        _headers = {"Accept": "text/turtle"}
        _from = component['from']
        _to = component['to'] + '.ttl'

        r = requests.get(_from, headers=_headers, allow_redirects=False, timeout=2)
        if r.headers.get('Location') == _to:
            # check that the content type is set correctly
            if r.headers['Content-Type'] is not 'text/turtle':
                passed = False
                fail_reasons.append(f'{_from} Response for turtle by content negotiation does not have Content-Type set to text/turtle')
            else:
                # check that the RDF is parsable and that it contains the expected title
                result = self.is_rdf_parsable(self, r, uri, component['title'], 'text/turtle')
                if not result['titleFound']:
                    passed = False
                    theFoundTitle = result['title']
                    fail_reasons.append(f'{_from} RDF title found as \'{theFoundTitle}\'' + result['message'])
        else:
            passed = False
            fail_reasons.append(
                'For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(component['label'],
                                                                                                 _from,
                                                                                                 _to, str(
                        r.headers.get('Location'))))
        ## END of turtle conneg

        Rule.__init__(
            self,
            metadata['name'],
            'Validate expected RDF',
            metadata['authority'],
            passed,
            fail_reasons,
            total_components,
            len(fail_reasons)
        )

    def is_rdf_parsable(self, r, uri, expected_title, formatType):
        # check the result is parseable RDF
        g = None
        try:
            g = rdflib.Graph().parse(data=r.content.decode('utf-8'), format=formatType)
        except Exception as e:
            print(e)

        if g is None:
            raise AssertionError(f'RDF {formatType} result is not parsable')

        # define namespaces
        RDFS = rdflib.namespace.RDFS
        XSD = rdflib.namespace.XSD
        SKOS = rdflib.namespace.SKOS

        # dict of result to return
        result = {'titleFound': False}

        # test to get title string
        for s, p, o in g.triples((rdflib.URIRef(uri), RDFS.label, None)):
            if o is not None:
                if o.value == expected_title:
                    result['titleFound'] = True
                result['title'] = o

        for s, p, o in g.triples((None, SKOS.prefLabel, None)):
            if o is not None:
                if o.value == expected_title:
                    result['titleFound'] = True
                result['title'] = o

        for s, p, o in g.triples((None, SKOS.label, None)):
            if o is not None:
                if o.value == expected_title:
                    result['titleFound'] = True
                result['title'] = o

        result['message'] = 'Parsable RDF response does not contain correct ontology title (?o  a owl:Ontology ; rdfs:label ?title .) or the expected title did not match.'

        return result   # returns the title that was found and whether it succeeded or not
                        # result['title'] = the title that was found
                        # result['titleFound'] = the bool if title was found


# class ValidateTurtleResponse(Rule):
#     """Validate the RDF Content-type as text/turtle and that the title in the RDF document matches the expected title.
#     """
#
#     def __init__(self, uri:str, metadata:dict, component:list):
#         """Constructor
#
#         Arguments:
#             uri {str} -- The URI.
#             metadata {dict} -- The metadata of the test.
#             component {list} -- The component containing the expected title.
#         """
#
#         passed = True
#         fail_reasons = []
#
#          # get the RDF version of the resource, using Content Negotiation
#         r = requests.get(uri, headers={'Accept': 'text/turtle'})
#
#         # check Content-Type
#         # assert 'text/turtle' in r.headers['Content-Type'], \
#         #     'Response for RDF by Content Negotiation does not have Content-Type set to text/turtle.'
#         if r.headers['Content-Type'] == 'text/turtle':
#             pass
#         else:
#             passed = False
#             fail_reasons.append('Response for RDF by Content Negotiation does not have Content-Type set to text/turtle.')
#
#         # get the RDF version of the resource, using Query String Arguments
#         r = requests.get(uri + '?_format=text/turtle')
#
#         # check Content-Type
#         # assert 'text/turtle' in r.headers['Content-Type'], \
#         #     'Response for RDF by _format Query String Argument does not have Content-Type set to text/turtle.'
#         if r.headers['Content-Type'] == 'text/turtle':
#             pass
#         else:
#             passed = False
#             fail_reasons.append('Response for RDF by _format Query String Argument does not have Content-Type set to text/turtle.')
#
#         # get the RDF version of the resource, using file extension-like syntax
#         r = requests.get(uri  + '.ttl')
#
#         # check Content-Type
#         # assert 'text/turtle' in r.headers['Content-Type'], \
#             # 'Response for RDF by file extension does not have Content-Type set to text/turtle.'
#         if r.headers['Content-Type'] == 'text/turtle':
#             pass
#         else:
#             passed = False
#             fail_reasons.append('Response for RDF by file extension does not have Content-Type set to text/turtle.')
#
#
#         result = is_rdf_parseable(r, uri, expected_title, 'text/turtle')
#         print(f'Title found: {result}')


class ValidateHTML(Rule):
    """Validate the HTML Content-type and title tag of the PID URI.
    """

    def __init__(self, uri:str, metadata:dict, component:list):
        """Constructor
        
        Arguments:
            Rule {Rule} -- The Rule parent class.
            uri {str} -- The URI.
            metadata {dict} -- The metadata of the test.
            component {list} -- The component containing the expected title.
        """

        passed = True
        fail_reasons = []

        # check the redirect
        r = requests.get(component['from'], headers={}, allow_redirects=False, timeout=2)
        if (r.headers.get('Location') == component['to']):
            pass
        else:
            passed = False
            fail_reasons.append(
                'For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(component['label'],
                                                                                                 component['from'],
                                                                                                 component['to'], str(
                        r.headers.get('Location'))))

        # get the HTML version of the resource
        r = requests.get(uri)

        # check Content-Type
        if r.headers['Content-Type'] == 'text/html':
            pass
        else:
            passed = False
            fail_reasons.append('Response for HTML does not have Content-Type set to text/html.')

        # check for HTML title ""
        expected_title = component['title']
        parsed_html = BeautifulSoup(r.content.decode('utf-8'), features="html.parser")
        received_title = parsed_html.head.find('title').text
        if expected_title  == received_title:
            pass
        else:
            passed = False
            fail_reasons.append('HTML response does not contain the correct <title> element. Expected "{}" got "{}"'.format(expected_title, received_title))

        Rule.__init__(
            self,
            metadata['name'],
            'Validate expected HTML',
            metadata['authority'],
            passed,
            fail_reasons,
            1, # total components
            len(fail_reasons)
        )


class ValidateComponent(Rule):
    """Validate that the PID URI test contains the correct component keys.
    
    Arguments:
        Rule {[type]} -- [description]
    """

    def __init__(self, uri, component:list):
        passed = True
        fail_reasons = []

        # required component keys
        required = [
            'label',
            'from',
            'to',
            'title',
            'rules',
            'headers'
        ]

        for req in required:
            if not req in component:
                fail_reasons.append(f'The \'{req}\' component is missing for {uri}')

        if fail_reasons:
            passed = False

        Rule.__init__(
            self,
            'Components for AGLDWG PID URI',
            'Validate that the AGLDWG PID URI contains required metadata for validation checking.',
            'AGLDWG',
            passed,
            fail_reasons,
            len(required),
            len(fail_reasons)
        )


class ValidateRedirect(Rule):
    #TODO: This is not currently used
    """Validate expected redirect route from a location to a destination. Redirects consider HTTP headers for content negotiation.
    """

    def __init__(self, metadata:dict, component:list):
        """Constructor
        
        Arguments:
            Rule {Rule} -- The Rule parent class.
            metadata {dict} -- The metadata of the test.
            component {list} -- The URL location, destination and header information.
        """

        passed = True
        fail_reasons = []

        r = requests.get(component['from'], headers=component['headers'], allow_redirects=False, timeout=2)
        if(r.headers.get('Location') == component['to']):
            pass
        else:
            passed = False
            fail_reasons.append('For test \'{}\', URI {} did not redirect to {} as expected, instead {}.'.format(component['label'], component['from'], component['to'], str(r.headers.get('Location'))))

        Rule.__init__(
            self,
            metadata['name'],
            'Validate correct HTTP redirections.',
            metadata['authority'],
            passed,
            fail_reasons,
            1, # total components
            len(fail_reasons)
        )


class ValidateMetadataIsPresent(Rule):
    def __init__(self, uri:str, data:dict):
        passed = True
        fail_reasons = []

        if not "metadata" in data:
            fail_reasons.append(f'The metadata field is missing for URI {uri}')

        if fail_reasons:
            passed = False

        Rule.__init__(
            self,
            'Metadata field is present for AGLDWG PID URI',
            'Validate that the AGLDWG URI contains a field named \'metadata\'',
            'AGLDWG',
            passed,
            fail_reasons,
            1,
            len(fail_reasons)
        )


class ValidateMetadata(Rule):
    """Validate that the PID URI test contains the required metadata.
    """

    def __init__(self, uri:str, metadata:dict):
        """Constructor
        
        Arguments:
            uri {str} -- [The URI's metadata to be tested.]
            metadata {dict} -- [The metadata.]
        """

        passed = True
        fail_reasons = []

        # required metadata fields
        required = [
            'name', 
            'authority'
        ]

        for req in required:
            if not req in metadata:
                fail_reasons.append(f'The \'{req}\' metadata is missing for URI {uri}')
        
        if fail_reasons:
            passed = False

        Rule.__init__(
            self,
            'Metadata for AGLDWG PID URI',
            'Validate that the AGLDWG PID URI contains required metadata for validation checking.',
            'AGLDWG',
            passed,
            fail_reasons,
            len(required),
            len(fail_reasons)
        )