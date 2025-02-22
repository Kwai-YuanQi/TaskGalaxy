import json
import sys
import os
from tqdm import tqdm
import random
import re
# from utils import mkdir, check_fin, get_alre, ROOT_DIR, is_contains_chinese
# sys.path.insert(0, ROOT_DIR)

sys.path.insert(0, "/hetu_group/huyifei/work_dir/archive/tools/apis/gpt_4v_api")
from gpt_4v_api import GPT_4v

def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    if pattern.search(text):
        return True
    else:
        return False

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
        return s[first_open:(last_close+1)].replace('\n', '').replace(' ', '')
    else:
        return None  # 如果 { 在 } 之后，返回 None


# gpt_4v = GPT_4v("liuchangyi_1eef47c1_gpt-4o-2024-05-13")
# gpt_4v = GPT_4v('zhangtianke_b62c-d1ce_gpt-4o-2024-05-13')
def gpt4o_process_(inp, output_file):
    try:
        gpt_4v = GPT_4v('wenbin_93bc5129_gpt-4o-2024-05-13')
        image_path, prompt, json_dict = inp
        question, answer = gpt_4v.vision(image_path, prompt, max_cycle=20)
        if question is not None and 'None' not in answer:
            if '~' in answer:
                item = {}
                item['image_path'] = json_dict['image_path']
                item['prompt'] = question
                item['gpt4o_output'] = answer
                with open(output_file, 'a') as f_write:
                    f_write.write("{}\n".format(json.dumps(item, ensure_ascii=False)))
                    f_write.flush()
    except:
        pass

def run_caption(input_file, output_file):
    src = []
    exsit = []
    # for data in open(output_file, 'r'):
    #     try:
    #         exsit.append(json.loads(data)['image_path'])
    #     except:
    #         continue
    # for line in open(input_file, 'r'):
    #     try:
    #         if json.loads(line)['image_path'] not in exsit:
    #             src.append(json.loads(line))
    #         else:
    #             continue
    #     except:
    #         print('异常!')
    for data in open(input_file, 'r'):
        try:
            src.append(json.loads(data))
        except:
            continue
    # src = json.loads(open(input_file, 'r'))
    # gpt4v 的输出内容可能不是标准的 json 格式，在 process_ 函数中不会被写入. 因此增加检查是否完成的逻辑
    total_retry_num = 0
    input_list = []
    # src = src[]
    for json_dict in tqdm(src):
        # image_path = json_dict["images"]
        # question = json_dict["question"]
        image_path = json_dict["image_path"]
        task_type = json_dict['related_task_type']
        all_task = "“"
        for task in task_type:
            all_task += task + "“,"
        question = 'You are a multimodal content understanding expert. Given an image and multiple task labels related to multimodal content understanding, with task labels as: “%s”. I would like to generate some question-answer pairs related to these task labels based on the image content. However, some task labels might not be relevant to the image content and thus cannot generate relevant questions. Please fully understand the image content and the meanings of the task labels, and select all the task labels that are appropriate for this task. Ensure the task labels are the same as the original. The output format should be: [task labels], without any other characters. If there are no matches, output [None].'
        question = question % all_task
        input_list.append((image_path, question, json_dict))

    print(len(input_list))
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=30)
    for inp in input_list:
        executor.submit(gpt4o_process_, inp, output_file)
    print('Waiting for all subprocesses done...')
    executor.shutdown(wait=True)
    print('All subprocesses done.')

    
if __name__ == "__main__":
    input_file='TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset.json'
    run_caption(input_file, "TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o.json")