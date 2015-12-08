import sys
import json
import config

cfg = config.load_config()
db = config.get_db(cfg)
table = config.get_table(db, cfg)
response = table.scan()
items = response['Items']
with open('dumptable.json', 'w') as fp:
    json.dump(items, fp)
