import json

with open("human_reviewed/human_approved_output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(json.dumps(data, indent=4, ensure_ascii=False))
