s_a = 'hello world'
print(s_a)

s = '{"a": "1", "b": "one"}'
# json 파일 저장
with open('test.json', 'wt') as file:
    json.dump(s, file, indent=4, sort_keys=True)

# json to 메모리(dict)
dic = json.dumps(s)

# jeon 파일 읽기
with open('test.json', 'rt') as file:
    s = json.load(file)

# json from 메모리(str)
s = json.loads(dic)
    