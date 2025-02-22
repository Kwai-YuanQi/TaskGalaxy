import json
init_file = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o.json','r')
output_file = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_forqa.json','w')
json_data = []
for line in init_file:
    try:
        json_data.append(json.loads(line))
    except:
        continue
from tqdm import tqdm
for data in tqdm(json_data):
    item = {}
    item['image_path'] = data['image_path']
    trimmed_string = data['gpt4o_output'][1:-1]
    lst = [item.replace("\"","").replace("“","").strip() for item in trimmed_string.split(',')]
    item['task_type'] = lst
    output_file.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
    output_file.flush()

    