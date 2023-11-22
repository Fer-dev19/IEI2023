import json
with open('./datos_json_MUR.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for entry in data:
        print(entry['email'])