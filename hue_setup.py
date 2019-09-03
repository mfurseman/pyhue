import pyhue
import collections

ADDRESS = "192.168.0.2"
API_KEY = "8q2z5320JbwclaU7Pa3it3qDOuUPrx4HeuP8NP0D"


Function = collections.namedtuple("Function", ["name", "value", "action"])


DIMMER_SWITCHES = [
    "Hallway Switch 1",
    "Hallway Switch 2",
    "Landing Switch 1",
    "Landing Switch 2",
    ]
DIMMER_SWITCH_FUNCTIONS = [
    Function("On", 1002, {"on": True}),
    Function("Off", 4002, {"on": False}),
    Function("Fully Bright", 1003, {"on": True, "bri": 255, "ct": 210}),
    Function("Dim Up", 2001, {"bri_inc": 30, "ct_inc": -30}),
    Function("Dim Down", 3001, {"bri_inc": -30, "ct_inc": 30}),
]

# Lights grouped by room
LIVING_ROOM_LIGHTS = [
    "RGB Strip"
    "White Strip"
    "Reading Light"
    "PS Lamp"
    "Floorstanding Lamp"
]
BEDROOM_LIGHTS = [
    "Bedside Lamp 1"
    "Bedside Lamp 2"
]
HALLWAY_LIGHTS = [
    "Landing Light 1"
    "Landing Light 2"
    "Landing Light CT"
    "Hallway Lamp"
    "Hallway Front 1"
    "Hallway Front 2"
    "Hallway Front CT"
    "Hallway Rear 2"
    "Hallway Rear 1"
    "Hallway Rear CT"
]


ESP_NAME = 'ESP8266-1'

#HALLWAY_LIGHTS = 'Hallway & Landing'


def upload_rule(hue, sensor_name, rule_name, queryable, button_value, action_body):
    sensor_id = hue.id_from_name(pyhue.SENSORS, sensor_name)
    rule_data = pyhue.build_rule(
        name=rule_name,
        conditions=[
            pyhue.build_condition(
                address="/{}/{}/state/{}".format(pyhue.SENSORS, sensor_id, queryable),
                operator='eq',
                value=str(button_value)),
            pyhue.build_condition(
                address="/{}/{}/state/lastupdated".format(pyhue.SENSORS, sensor_id),
                operator='dx')],
        actions=[
            pyhue.build_action(
                address="/groups/0/action",
                method="PUT",
                body=action_body)])
    hue.create_entry(pyhue.RULES, rule_data)


hue = pyhue.Hue(ADDRESS, API_KEY)
if __name__ == "__main__":
    # Teardown rules
    rules = hue.get_rules()
    for key in rules:
        hue.delete_entry(pyhue.RULES, key)

    # Make rules for ESP8266
    upload_rule(hue, ESP_NAME, '{}-{}'.format(ESP_NAME, "On"), 'status', 16771095, {"on": True})
    upload_rule(hue, ESP_NAME, '{}-{}'.format(ESP_NAME, "Off"), 'status', 16738455, {"on": False})

    # Make rules for each dimmer
    for switch_name in DIMMER_SWITCHES:
        for function in DIMMER_SWITCH_FUNCTIONS:
            rule_name ='{}-{}'.format(switch_name, function.name)
            upload_rule(hue, switch_name, rule_name, 'buttonevent', function.value, function.action)
