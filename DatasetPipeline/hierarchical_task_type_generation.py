import json
import sys
import os
from tqdm import tqdm
sys.path.append('/hetu_group/liuchangyi/mllm/code/atomCaption/caption/')
sys.path.insert(0, "/hetu_group/huyifei/work_dir/archive/tools/apis/gpt_4v_api")
sys.path.insert(0, "/hetu_group/chenjiankang/research")
from utils import mkdir, check_fin, get_alre, ROOT_DIR, is_contains_chinese
# from gpt_4v_api import GPT_4v
from mmu_chat_gpt_pb2 import MmuChatGptRequest,MmuChatGptResponse
from mmu_chat_gpt_pb2_grpc import (
    MmuChatGptServiceStub,
)
# from mmu.media_common_pb2 import ImgUnit
import time
from PIL import Image
import io
from io import BytesIO
import requests
import base64
from kess.framework import (
    ClientOption,
    GrpcClient,
    KessOption,
)

from collections import defaultdict
import pandas as pd

def check_(output_file):
    if not os.path.exists(output_file): return []
    f = open(output_file)
    done_list = []
    for line in f.readlines():
        js = json.loads(line)
        if 'index' in js: 
            done_list.append(js['index'])
        elif "pid" in js:
            done_list.append(js['pid'])
        else:
            done_list.append(js['key'])
    return done_list

client_option = ClientOption(
                    biz_def='mmu',
                    grpc_service_name='mmu-chat-gpt-service',
                    grpc_stub_class=MmuChatGptServiceStub,
                )
grpc_client = GrpcClient(client_option)



def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def openai_api(image_paths, prompt, max_cycle=4):
    count = 1
    if isinstance(image_paths, str):
        image_paths = [image_paths]
    while max_cycle > 0:
        print("try {} times".format(count))
        try:
            # GPT4o-text
            content = [{ "type": "text",
                        "text": prompt}]
            # GPT4o-image-text
            # base64_images = [encode_image(image_path) for image_path in image_paths]
            # if '<image>' in prompt: # 多图
            #     content = [{ "type": "text",
            #                 "text": prompt.split('<image>')[0]}]
            #     for ppt, base64_image in zip(prompt.split('<image>')[1:], base64_images):
            #         content.append({"type": "image_url",
            #             "image_url": {
            #             "url": f"data:image/jpeg;base64,{base64_image}"
            #             }})
            #         content.append({ "type": "text",
            #                 "text": ppt})
            # content = []
            # for base64_image in base64_images:
            #     content.append({"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
            # content.append({ "type": "text","text": prompt})
            # else: # 单图
            #     content = []
            #     for base64_image in base64_images:
            #         content += [{"type": "image_url",
            #                 "image_url": {
            #                 "url": f"data:image/jpeg;base64,{base64_image}"
            #                 }}]
                        
            #     content += [{ "type": "text",
            #                 "text": prompt}]
            messages = [
                {
                    "role": "user",
                    "content": content
                }
            ]

            # biz = "wenbin_93bc5129_gpt-4o-2024-05-13"
            biz = "chenkaibing_3a18b4c3_gpt-4o-2024-05-13"
            request = MmuChatGptRequest(biz=biz)
            request.req_id = 'test_1000'
            request.session_id = 'test'
            request.query = json.dumps(messages)
            request.config['messages'] = 'True'
            request.config['max_tokens'] = '4096'
            timeout=180
            resp = grpc_client.Chat(request, timeout=timeout)
            json_text = resp.answer
            cur_json = json.loads(json_text)
            output = cur_json["choices"][0]["message"]["content"]
            return output
        except Exception as e:
            print("Error occurred, retry")
            print(e)
            max_cycle -= 1
        count += 1
        time.sleep(15)
    return None


def gpt4o_process_(inp):
    # image_path, prompt, json_dict = inp
    # # prompt += "\n\nPlease give your answer with the format 'The answer is: \n' in the first line."
    # answer = openai_api(image_path, prompt, 2)
    # if answer is not None:
    #     # if is_contains_chinese(answer):
    #     json_dict['model_output'] = answer
    #     # json_dict['model_judge'] = answer
    #     with open(output_file, 'a') as f_write:
    #         f_write.write("{}\n".format(json.dumps(json_dict, ensure_ascii=False)))
    prompt = inp
    answer = openai_api(None, prompt, 2)
    print(answer)
    if answer is not None:
        for ans in answer.split('\n'):
            p = '/TaskGalaxy/DatasetPipeline/TaskType'
            if '~' in ans:
                ans.lower()
                lines = ans.split('~')
                for line in lines:
                    p = os.path.join(p, line)
                os.makedirs(p)
            else:
                p = os.path.join(p, ans)
                os.makedirs(p)




# def gpt4o_process_(prompt):
#     gpt_4v = GPT_4o('wenbin_93bc5129_gpt-4o-2024-05-13')
#     question, answer = gpt_4v.vision(None, prompt, max_cycle=20)
#     print(answer)
#     if answer is not None:
#         for ans in answer.split('\n'):
#             p = '/mllm_hdd/chenjiankang/Chinese-Taskgalaxy/Tasktype'
#             if '~' in ans:
#                 ans.lower()
#                 lines = ans.split('~')
#                 for line in lines:
#                     p = os.path.join(p, line)
#                 os.makedirs(p)
#             else:
#                 p = os.path.join(p, ans)
#                 os.makedirs(p)
                    

def get_level(input_dir, task_num):
    task_list = []
    task_first= []
    for p in os.listdir(input_dir):
        task_first.append(p) # 所有的一级类目
    # 获取二级目录
    task_second = []
    for task_f in task_first:
        for pp in os.listdir(os.path.join(input_dir, task_f)):
            task_second.append(task_f+'~'+pp)
    # # 获取三级目录
    task_three = []
    for task_s in task_second:
        for pp in os.listdir(os.path.join(input_dir, task_s.split('~')[0], task_s.split('~')[1])):
            task_three.append(task_s+'~'+pp)
    # # 获取四级目录
    task_four = []
    for task_f in task_three:
        for pp in os.listdir(os.path.join(input_dir, task_f.split('~')[0], task_f.split('~')[1], task_f.split('~')[2])):
            task_four.append(task_f+'~'+pp)
    if task_num == 1:
        task_list = task_first
    elif task_num == 2:
        task_list = task_second
    elif task_num == 3:
        task_list = task_three
    elif task_num == 4:
        task_list = task_four
    return task_list


def run_caption(input_dir, task_num):    
    task_list = get_level(input_dir, task_num)
    print(len(task_list))
    input_list = []
    if task_num == 1:
        # 一级类目
        question = "You are an expert in multimodal content understanding with extensive experience in this field. I would like to construct a comprehensive task labeling system related to multimodal content understanding that includes only two modalities: images and text. In this system, the input consists of images and corresponding text, and the output is in the form of text. I want to start constructing this system from the first-level task categories. Currently, dozens of first-level task categories have already been established by humans, which are:'%s' Please expand and supplement with new first-level categories that do not belong to the aforementioned categories to ensure comprehensive coverage of all task categories in multimodal content understanding scenarios. Output format: Each line should correspond to one category, without any other characters."
        task_list_str = ""
        for task in task_list:
            task_list_str += task+'\n'
        question = question%task_list_str
        input_list.append(question)
    elif task_num == 2:
        # 二级类目   
        task_first = get_level(input_dir, 1)
        task_second = get_level(input_dir, 2)
        for task_f in task_first:
            question_1 = "You are an expert in multimodal content understanding with extensive experience in this field. I want to construct a comprehensive task label system related to multimodal content understanding, which only includes image and text modalities. In this system, the input is an image and the corresponding text, and the output is in the form of text. The primary and secondary categories are connected by '∼'. The task name of the primary category that needs to be detailed currently is '%s', and multi- ple secondary categories have already been established manually for this primary category, which are: '%s'. Please supplement other categories that do not belong to the aforementioned secondary categories to cover all task scenarios under the primary category of multi-modal content understand- ing. Output format: Each line corresponds to one task category, without any other characters, and different levels of task categories are connected by '~'."
            question_2 = "You are an expert in multimodal content understanding with extensive experience in this field. I want to construct a comprehensive task label system related to multimodal content understanding, which only includes image and text modalities. In this system, the input is an image and the corresponding text, and the output is in the form of text. The primary and secondary categories are connected by '∼'. The task name of the primary category that needs to be detailed currently is '%s'. Please expand the secondary task categories under this primary task category to cover all tasks included in this primary task category in the context of multimodal content understanding. Output format: Each line corresponds to one task category, without any other characters, and different levels of task categories are connected by '∼'."
            task_sforf = []
            flag_s = False
            for task_s in task_second:
                if task_f in task_s:#有二级类目
                    flag_s = True
                    for task_s in task_second: #找所有二级类目
                        if task_f in task_s:
                            task_sforf.append(task_s.split('~')[1])                        
                    task_se = ""
                    for t in task_sforf:
                        task_se += t + '\n'
                    question_1 = question_1 % (task_f, task_se)
                    input_list.append(question_1)
                    break
            if flag_s is False:#没有二级类目
                question_2 = question_2 % task_f
                input_list.append(question_2)
    elif task_num == 3:
        #三级类目
        task_second = get_level(input_dir, 2)
        task_three = get_level(input_dir, 3)
        for task_s in task_second:
            question_1 = "You are an expert in multimodal content understanding with extensive experience in this field. I want to construct a comprehensive task taxonomy for multimodal content understanding that in- cludes only two modalities: images and text. The input to this taxonomy will be images and their corresponding text, and the output will be in text form. The primary, secondary, and tertiary cate- gories in this taxonomy are connected by '~'. Currently, the task name for the secondary category that needs to be detailed is '%s', and several tertiary categories have already been established man- ually for this secondary category, which are: '%s'. Please supplement additional categories that do not belong to the aforementioned tertiary categories to cover all tasks under the secondary category in the context of multimodal content understanding. Output format: Each line should correspond to one task category, without any other characters. Different levels of task categories should be connected by '~'."
            question_2 = "You are an expert in multimodal content understanding with extensive experience in this field. I want to construct a comprehensive task taxonomy for multimodal content understanding that in- cludes only two modalities: images and text. The input to this taxonomy will be images and their corresponding text, and the output will be in text form. The primary, secondary, and tertiary cate- gories in this taxonomy are connected by '~'. Currently, the task name for the secondary category that needs to be detailed is '%s'. Please expand the tertiary task categories under this secondary task category to cover all tasks included in this secondary task category in the context of multimodal content understanding. Output format: Each line should correspond to one task category, without any other characters. Different levels of task categories should be connected by '~'."
            task_tfors = []
            flag_t = False
            for task_t in task_three:
                if task_s in task_t:#有三级类目
                    flag_t = True
                    for task_tall in task_three:#找所有三级类目
                        if task_s in task_tall:
                            task_tfors.append(task_tall.split('~')[2])
                    task_th = ""
                    for t in task_tfors:
                        task_th += t + '\n'
                    question_1 = question_1 % (task_s, task_th)
                    input_list.append(question_1)
                    break
            if flag_t is False:#没有三级目录
                question_2 = question_2 % task_s
                input_list.append(question_2)
    print(len(input_list))
    # from multiprocessing import Pool
    # p = Pool(6)
    # for inp in input_list:
    #     p.apply_async(gpt4o_process_, args=(inp, ))
    # print('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    # print('All subprocesses done.')
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=30)
    for inp in input_list:
        executor.submit(gpt4o_process_, inp)
        # gpt4o_process_(inp, output_file)
    print('Waiting for all subprocesses done...')
    executor.shutdown(wait=True)
    print('All subprocesses done.')

if __name__ == "__main__":
    for i in range(1):
        run_caption('/TaskGalaxy/DatasetPipeline/Tasktype', 3)
