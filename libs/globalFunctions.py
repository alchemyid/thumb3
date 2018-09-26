import json


def flat(*nums):
    return tuple(int(round(n)) for n in nums)

def read_config(json_node, string):
    with open('config.json') as json_data:
        if string is None:
            d = json.load(json_data)
            return d[json_node]
        else:
            d = json.load(json_data)
            return d[json_node][string]