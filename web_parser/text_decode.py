import json

with open("test.json") as f:
    s = f.read()
    a = s[0:-2] + "]"
    a = json.loads(a)
    with open('data.json', 'w') as f2:
        json.dump(a, f2)