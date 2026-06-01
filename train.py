import json

with open("transcripts.json") as f:
    dataset = json.load(f)

for item in dataset:
    print(item["transcript"])