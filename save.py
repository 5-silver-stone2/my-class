import json

data = [
    {
        'title':'어린 왕자',
        'author':'생텍쥐페리'
    }
]
with open('books.json','w',encoding='utf-8') as file:
    json.dump(
        data,
        file,
        ensure_ascii=False,
        indent=4
    )