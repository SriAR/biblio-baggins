import json

def pp(data, sort_keys=False):
    return json.dumps(data, indent=4, sort_keys=sort_keys)
