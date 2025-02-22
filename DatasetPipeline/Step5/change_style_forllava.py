import json
import uuid
    
json_data = []
init_file = open('TaskGalaxy/DatasetPipeline/taskgalaxy_.json', 'r')
for line in init_file:
    json_data.append(json.loads(line))

wtask_for_llava = open('TaskGalaxy/DatasetPipeline/taskgalaxy_llava.json', 'w')
wtaskdata = []
for data in json_data:
    entry_id = str(uuid.uuid4())
    item = {
        "id": entry_id,
        "image": data['image_path'],
        "task_type": data['task_type'],
        "conversations": [
            {"from": "human", "value": "<image>\n" + data['question']},
            {"from": "gpt", "value": data['answer']}
        ]
    }
    wtaskdata.append(item)

wtask_for_llava.write('{}\n'.format(json.dumps(wtaskdata, ensure_ascii=False, indent=2)))   


