# TODO

## Validate RDF Ruleset
* Change the `ValidateTurtleResponse` class to a general class that tests for all supported RDF types. 

  * Supported RDF types are listed here: https://rdflib.readthedocs.io/en/stable/plugin_parsers.html?highlight=format

* Modify the `ValidateComponent` class so that it ensures the component property has an `"rdf"` property containing the supported RDF types as keys and its value as booleans. This is true only if the rules array contains `"rdf"`. 