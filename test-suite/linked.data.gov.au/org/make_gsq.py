import json

iris_http = [
    "http://linked.data.gov.au/def/address-type",
    "http://linked.data.gov.au/def/anzsic-2006",
    "http://linked.data.gov.au/def/australian-phone-area-codes",
    "http://linked.data.gov.au/def/australian-states-and-territories",
    "http://linked.data.gov.au/def/borehole-design",
    "http://linked.data.gov.au/def/borehole-drilling-method",
    "http://linked.data.gov.au/def/borehole-purpose",
    "http://linked.data.gov.au/def/borehole-start-point",
    "http://linked.data.gov.au/def/borehole-status",
    "http://linked.data.gov.au/def/borehole-status-event",
    "http://linked.data.gov.au/def/borehole-sub-purpose",
    "http://linked.data.gov.au/def/countries",
    "http://linked.data.gov.au/def/data-access-rights",
    "http://linked.data.gov.au/def/dataciteroles",
    "http://linked.data.gov.au/def/depth-reference",
    "http://linked.data.gov.au/def/earth-science-data-category",
    "http://linked.data.gov.au/def/geo-commodities",
    "http://linked.data.gov.au/def/geo-product-form",
    "http://linked.data.gov.au/def/geoadminfeatures",
    "http://linked.data.gov.au/def/geological-observation-instrument",
    "http://linked.data.gov.au/def/geological-observation-method",
    "http://linked.data.gov.au/def/geological-observation-type",
    "http://linked.data.gov.au/def/geological-properties",
    "http://linked.data.gov.au/def/geological-sites",
    "http://linked.data.gov.au/def/geometry-roles",
    "http://linked.data.gov.au/def/georesource-report",
    "http://linked.data.gov.au/def/geou",
    "http://linked.data.gov.au/def/gsq-alias",
    "http://linked.data.gov.au/def/gsq-dataset-theme",
    "http://linked.data.gov.au/def/gsq-feature-status",
    "http://linked.data.gov.au/def/gsq-roles",
    "http://linked.data.gov.au/def/gsq-sample-facility",
    "http://linked.data.gov.au/def/iso-4217-currencies",
    "http://linked.data.gov.au/def/iso11179-6/RolesAndResponsibilities",
    "http://linked.data.gov.au/def/iso19115-1/RoleCode",
    "http://linked.data.gov.au/def/iso639-1",
    "http://linked.data.gov.au/def/lithotype",
    "http://linked.data.gov.au/def/minerals",
    "http://linked.data.gov.au/def/observation-detail-type",
    "http://linked.data.gov.au/def/organisation-activity-status",
    "http://linked.data.gov.au/def/organisation-name-types",
    "http://linked.data.gov.au/def/organisation-type",
    "http://linked.data.gov.au/def/party-identifier-type",
    "http://linked.data.gov.au/def/party-relationship",
    "http://linked.data.gov.au/def/qesd-qkd",
    "http://linked.data.gov.au/def/qesd-uom",
    "http://linked.data.gov.au/def/qg-agent",
    "http://linked.data.gov.au/def/qg-file-types",
    "http://linked.data.gov.au/def/qg-sites",
    "http://linked.data.gov.au/def/qld-data-licenses",
    "http://linked.data.gov.au/def/qld-export-terminals",
    "http://linked.data.gov.au/def/qld-resource-permit",
    "http://linked.data.gov.au/def/qld-resource-permit-status",
    "http://linked.data.gov.au/def/qld-utm-zones",
    "http://linked.data.gov.au/def/qualitative-confidence",
    "http://linked.data.gov.au/def/queensland-crs",
    "http://linked.data.gov.au/def/report-detail-type",
    "http://linked.data.gov.au/def/report-status",
    "http://linked.data.gov.au/def/resource-project-lifecycle",
    "http://linked.data.gov.au/def/resource-stockpile-purpose",
    "http://linked.data.gov.au/def/resource-types",
    "http://linked.data.gov.au/def/result-type",
    "http://linked.data.gov.au/def/sample-detail-type",
    "http://linked.data.gov.au/def/sample-location-status",
    "http://linked.data.gov.au/def/sample-location-types",
    "http://linked.data.gov.au/def/sample-material",
    "http://linked.data.gov.au/def/sample-preparation-methods",
    "http://linked.data.gov.au/def/sample-relationship",
    "http://linked.data.gov.au/def/sample-type",
    "http://linked.data.gov.au/def/sampling-method",
    "http://linked.data.gov.au/def/seismic-dimensionality",
    "http://linked.data.gov.au/def/site-detail-type",
    "http://linked.data.gov.au/def/site-relationships",
    "http://linked.data.gov.au/def/site-status",
    "http://linked.data.gov.au/def/survey-detail-type",
    "http://linked.data.gov.au/def/survey-method",
    "http://linked.data.gov.au/def/survey-relationship-type",
    "http://linked.data.gov.au/def/survey-status",
    "http://linked.data.gov.au/def/survey-type",
    "http://linked.data.gov.au/def/telephone-type",
    "http://linked.data.gov.au/def/transaction-status",
    "http://linked.data.gov.au/def/transaction-type",
    "http://linked.data.gov.au/def/trs",
    "http://resource.geosciml.org/vocabulary/timescale/skos-demo",
    "http://www.w3.org/ns/time/gregorian",
]
iris_https = [
    "https://linked.data.gov.au/def/dataset-relationships",
    "https://linked.data.gov.au/def/geofeatures",
    "https://linked.data.gov.au/def/qesd-qkd",
    "https://linked.data.gov.au/def/qesd-uom",
    "https://linked.data.gov.au/def/qg-security-classifications",
    "https://linked.data.gov.au/def/qld-obsprop",
    "https://linked.data.gov.au/def/rock-unit-rank",
]

j = {}
for iri in iris_http:
    slug = iri.split("/")[-1]
    j[iri] = [
        {
            "label": slug + " HTML",
            "from": iri,
            "to": "https://vocabs.gsq.digital/object?uri=" + iri,
            "headers": {}
        },
        {
            "label": slug + " Turtle",
            "from": iri,
            "to": "https://vocabs.gsq.digital/object?uri=" + iri + "&_mediatype=text/turtle",
            "headers": {"Accept": "text/turtle"}
        }
    ]

for iri in iris_https:
    slug = iri.split("/")[-1]
    j[iri] = [
        {
            "label": slug + " HTML",
            "from": iri,
            "to": "https://vocabs.gsq.digital/object?uri=" + iri,
            "headers": {}
        },
        {
            "label": slug + " Turtle",
            "from": iri,
            "to": "https://vocabs.gsq.digital/object?uri=" + iri + "&_mediatype=text/turtle",
            "headers": {"Accept": "text/turtle"}
        }
    ]

json.dump(j, open("gsq.json", "w"), indent=4)
