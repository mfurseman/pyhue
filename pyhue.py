import json
import requests


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


def build_condition(address, operator, value=None):
    condition = {
        "address": address,
        "operator": operator,
    }
    if value:
        condition["value"] = value
    return condition


def build_action(address, method, body):
    action = {
        "address": address,
        "method": method,
        "body": body,
    }
    return action


def build_rule(name, conditions, actions):
    rule_data = {
        "name": name,
        "conditions": conditions,
        "actions": actions,
    }
    return rule_data


class ApiException(Exception):
    pass


class Hue(object):

    def __init__(self, address, api_key):
        self._address = address
        self._api_key = api_key

    def get_rules(self):
        return self.json_get([RULES])

    def get_sensors(self):
        return self.json_get([SENSORS])

    def get_lights(self):
        return self.json_get([LIGHTS])

    def build_request(self, paths=[]):
        http_prefix = "http://{}/api/{}/".format(self._address, self._api_key)
        return http_prefix + "/".join(paths)

    def delete_entry(self, api_field, field_id):
        result = json.loads(requests.delete(self.build_request([api_field, str(field_id)])).text)
        if result[0].keys()[0] != 'success':
            raise ApiException(pretty_print(result))

    def json_get(self, paths=[]):
        return json.loads(requests.get(self.build_request(paths)).text)

    def create_entry(self, api_field, data):
        result = json.loads(requests.post(self.build_request([api_field]), data=json.dumps(data)).text)
        if result[0].keys()[0] == 'success':
            return result[0]['success']['id']
        else:
            raise ApiException(pretty_print(result))

    def id_from_name(self, api_field, name):
        tree = self.json_get(paths=[api_field])
        for key in tree:
            if tree[key]['name'] == name:
                return key
        raise LookupError('Error: ID not found for name {}'.format(name))
