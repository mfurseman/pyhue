import json
import requests


ADDRESS = "192.168.0.2"
API_KEY = "8q2z5320JbwclaU7Pa3it3qDOuUPrx4HeuP8NP0D"


RULES = 'rules'
SCENES = 'scenes'
LIGHTS = 'lights'
GROUPS = 'groups'
SHEDULES = 'shedules'
SENSORS = 'sensors'

API_FIELDS = [
    RULES,
    SCENES,
    LIGHTS,
    GROUPS,
    SHEDULES,
    SENSORS,
    ]


def pretty_print(obj):
    return json.dumps(obj, sort_keys=True, indent=4)


def build_request(paths=[]):
    http_prefix = "http://{}/api/{}/".format(ADDRESS, API_KEY)
    return http_prefix + "/".join(paths)


def json_get(paths=[]):
    return json.loads(requests.get(build_request(paths)).text)


def delete_entry(api_field, field_id):
    result = json.loads(requests.delete(build_request([api_field, str(field_id)])).text)
    if result[0].keys()[0] != 'success':
        raise ApiException(pretty_print(result))


class ApiException(Exception):
    pass


class Hue(object):

    def __init__(self):
        pass


tree = json_get()
#delete_entry(RULES, 1)
#print tree.keys()
#print tree[SENSORS]['12']
print pretty_print(tree[SENSORS]['12'])
#for rule_id in tree[RULES]:
    #pretty_print(tree[RULES][rule_id]['name'])
