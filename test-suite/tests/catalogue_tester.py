from enum import Enum
import requests


class ResourceType(Enum):
    Dataset = 'dataset'
    Ontology = 'ontology'
    Vocabulary = 'vocabulary'


def get_path(resource_type):
    if not isinstance(resource_type, ResourceType):
        raise ValueError(
            'The Resource Type argument must be one of {} but you said {}'.format(
                    ', '.join(ResourceType.__members__),
                    str(resource_type)
            )
        )

    # type ok so get list of things of that type
    r = requests.get(
        'http://catalogue.linked.data.gov.au/jsonapi/node/{}'.format(resource_type.value)
    )

    items = []
    for i in r.json()['data']:
        # only get Accepted resources
        # using the UUID Drupal ID for the term 'accepted'
        if i['relationships']['field_registry_status']['data']['id'] == '62894a33-4dc9-4544-8ddb-c9a99fb7709b':
            items.append(i['attributes']['field_agldwg_identifier'])

    return sorted(items)


if __name__ == '__main__':
    print(get_path(ResourceType.Dataset))
