import json

def decodeSequence(x):
    return json.loads(x)["sequence"]