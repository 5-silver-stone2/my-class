import json

data = [
    {
        'title':'컴퓨터',
        'date':'2026-09-01'
    }
]
with open('objects.json','w',encoding='utf-8') as file:
    json.dump(
        data,
        file,
        ensure_ascii=False,
        indent=4
    )