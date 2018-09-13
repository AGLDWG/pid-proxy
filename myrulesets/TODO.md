
## Validate RDF Ruleset
### TODO
* Support for testing other (optional) RDF types
* Convert the tests for other PIDs to the new format
* Attend to the failed tests (mostly the content-type not set for HTML)
### Current features
#### Validates that the required information is there for a given PID.
* Validates the metadata
* Validates the component fields
#### Tests for HTML and certain RDF types (currently only supports turtle)
* Validate HTML
  * Check the redirect
  * Check the content type
  * Check the HTML title
* Validate RDF
  * For file extension, query string arguments and content negotiation
    * Check the redirect
    * Check the content type
    * Check RDF is parsable
    * Check that the title in the RDF matches (supports rdfs:label, skos:prefLabel and skos:label)
#### A simpler format for new data has been established. Example:
```javascript
{
    "http://linked.data.gov.au/def/reg-status":
    {
        "metadata": {
            "name": "Registry Status Vocabulary",
            "authority": "AGLDWG"
        },
        "components": [
            {
               "label": "Registry Status Vocabulary",
               "from": "http://linked.data.gov.au/def/reg-status",
               "to": "http://www.linked.data.gov.au/def/reg-status",
               "title": "Registry Ontology's Status vocabulary",
               "rules": ["html", "rdf"],
               "headers": {
                 "turtle": {"Accept": "text/turtle"}
               }
            },
            {
               "label": "Registry Status Vocabulary, Concept accepted",
               "from": "http://linked.data.gov.au/def/reg-status/accepted",
               "to": "http://www.linked.data.gov.au/def/reg-status/accepted",
               "title": "Registry Ontology's Status vocabulary",
               "rules": ["html", "rdf"],
               "headers": {
                 "turtle": {"Accept": "text/turtle"}
               }
            }
         ]
    },

    "http://linked.data.gov.au/def/placenames":
    {
      "metadata": {
        "name": "Place Names Ontology",
        "authority": "Geoscience Australia"
      },
      "components": [
        {
          "label": "Place Names Ontology",
          "from": "http://linked.data.gov.au/def/placenames",
          "to": "http://www.linked.data.gov.au/def/placenames",
          "title": "Place Names Ontology",
          "rules": ["html", "rdf"],
          "headers": {
            "turtle": {"Accept": "text/turtle"}
          }
        }
      ]
    }
}
```

## Notes
  * Supported RDF types are listed here: 
    * https://rdflib.readthedocs.io/en/stable/plugin_parsers.html?highlight=format
  
  * Or perhaps only support the main types like it is listed here: 
    * http://www.easyrdf.org/converter
