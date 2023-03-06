s_a = 'hello world'
print(s_a)

import json
s소스 = '{"a": "1", "b": "one"}'

# str to dict
dic소스 = json.loads(s소스)

# json to 파일
with open(file='config.json', mode='wt', encoding='cp949') as file:
    json.dump(dic소스, file, indent=4, sort_keys=False, ensure_ascii=False)

# json from 파일
with open(file='config.json', mode='rt', encoding='cp949') as file:
    dic리드 = json.load(file)

# dict to str
s리드 = json.dumps(dic리드)
