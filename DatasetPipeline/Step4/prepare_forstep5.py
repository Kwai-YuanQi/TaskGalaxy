import json
import re
init_file = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa.json','r')
output_file = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa_forfilter.json','w')
json_data = []
for line in init_file:
    try:
        json_data.append(json.loads(line))
    except:
        continue

def extract_between_braces(s):
    # 找到第一个 { 的索引
    first_open = s.find('{')
    if first_open == -1:
        return None  # 如果没有找到 {，返回 None

    # 找到最后一个 } 的索引
    last_close = s.rfind('}')
    if last_close == -1:
        return None  # 如果没有找到 }，返回 None

    # 提取第一个 { 和最后一个 } 之间的部分
    if first_open < last_close:
        return s[first_open:(last_close+1)].replace('\n', '')
    else:
        return None  # 如果 { 在 } 之后，返回 None
from tqdm import tqdm
count = 0
for data in tqdm(json_data):
    item = {}
    item['image_path'] = data['image_path']
    output = data['gpt4o_output']
    output = extract_between_braces(output)
    try:
        output = re.findall(r'\{[^{}]*\}', output)
        for out in output:
            try:
                out = json.loads(out)
                item['task_type'] = out['task_type']
                item['question'] = out['question']
                item['answer'] = out['answer']
                output_file.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
                output_file.flush()
            except:
                continue
    except:
        continue
    # output_file.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
    # output_file.flush()

    