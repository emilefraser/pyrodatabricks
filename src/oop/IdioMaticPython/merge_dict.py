from typing import ChainMap


d1 = {
    "person1" : {
        "name": "shaun",
        "age" : None
    }
}

d2 = {
    "person1" : {
        "name": "shaun",
        "age" : 44,
        "pet" : "cat"
    },
    "person2" : {
        "name": "fin",
        "age": 5
    }
}

d3 = {
    "address": {
        "street": "courtney road",
        "house number": 76,
        "postcode": "BS15 9RH"
    }
}

import json

merged = ChainMap(d3, d2, d1)
merged = dict(ChainMap(d3, d2, d1))
merged = json.dumps(merged, indent=4)

print(merged)
