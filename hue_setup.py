import pyhue

ADDRESS = "192.168.0.2"
API_KEY = "8q2z5320JbwclaU7Pa3it3qDOuUPrx4HeuP8NP0D"


DIMMER_SWITCHES = [
    "Hallway Switch 1",
    "Hallway Switch 2",
    "Landing Switch 1",
    "Landing Switch 2",
    ]

HALLWAY_LIGHTS = 'Hallway & Landing'


#tree = hue.json_get()
#delete_entry(RULES, 1)
#print pyhue.pretty_print(tree[pyhue.SENSORS])

#hue.create_entry(pyhue.RULES, rule_data)
#print tree[SENSORS]['12']
#print pretty_print(tree[SENSORS]['12'])
#for rule_id in tree[RULES]:
    #pretty_print(tree[RULES][rule_id]['name'])

########################################################

hue = pyhue.Hue(ADDRESS, API_KEY)

rules = hue.get_rules()
esp_rules = {}
for rule_id in rules.keys():
    if 'ESP8266' in rules[rule_id]['name']:
        esp_rules[rule_id] = rules[rule_id]

# Teardown rules
not_esp_rules = set(rules.viewkeys()).difference(esp_rules.viewkeys())
for key in not_esp_rules:
    print 'Removing rule {}'.format(rules[key]['name'])
    hue.delete_entry(pyhue.RULES, key)

# Find the IDs for our dimmer switches
dimmer_switch_ids = []
for switch in DIMMER_SWITCHES:
    dimmer_switch_ids.append(hue.id_from_name(pyhue.SENSORS, switch))

# Make rules for each dimmer
hallway_lights = hue.id_from_name(pyhue.GROUPS, HALLWAY_LIGHTS)
sensors = hue.get_sensors()
for switch_id in dimmer_switch_ids:
    name = sensors[switch_id]['name']
    print 'Creating rules for switch {}'.format(name)
    rule_data = pyhue.build_rule(
        name='{} - {}'.format(name, 'Short On'),
        conditions=[
            pyhue.build_condition(
                address="/{}/{}/state/buttonevent".format(pyhue.SENSORS, switch_id),
                operator='eq',
                value='1002'),
            pyhue.build_condition(
                address="/{}/{}/state/lastupdated".format(pyhue.SENSORS, switch_id),
                operator='dx')],
        actions=[
            pyhue.build_action(
                address="/groups/0/action",
                method="PUT",
                body={"on": True})])
    hue.create_entry(pyhue.RULES, rule_data)

    rule_data['name'] = '{} - {}'.format(name, 'Short Off')
    rule_data['conditions'][0]['value'] = '4002'
    rule_data['actions'][0]['body']['on'] = False
    hue.create_entry(pyhue.RULES, rule_data)
