s_a = 'hello world'
print(s_a)

import json
s소스 = '{"a": "1", "b": "one"}'

# str to dict
dic소스 = json.loads(s소스)

# json to 파일
with open('config.json', 'wt') as file:
    json.dump(dic소스, file, indent=4, sort_keys=False)

# json from 파일
with open('config.json', 'rt') as file:
    dic리드 = json.load(file)

# dict to str
s리드 = json.dumps(dic리드)
