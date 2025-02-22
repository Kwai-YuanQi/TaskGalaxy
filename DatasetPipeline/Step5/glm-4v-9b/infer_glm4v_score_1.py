import torch
import json
import sys
import os
from tqdm import tqdm
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer

def glm4v_process(model, tokenizer, inp, output_file):
    image_path, prompt, json_dict = inp
    query = prompt
    image = Image.open(image_path).convert('RGB')
    inputs = tokenizer.apply_chat_template([{"role": "user", "image": image, "content": query}],
                                        add_generation_prompt=True, tokenize=True, return_tensors="pt",
                                        return_dict=True)  # chat mode
    inputs = inputs.to(device)
    gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        answer = tokenizer.decode(outputs[0]).split('<|endoftext|>')[0].strip()
        json_dict['model_output'] = answer
        with open(output_file, 'a') as f_write:
            f_write.write("{}\n".format(json.dumps(json_dict, ensure_ascii=False)))

def run_caption(model, tokenizer, input_file, output_file):
    src = []
    for line in open(input_file, 'r'):
        try:
            src.append(json.loads(line))
        except:
            print('异常!')
    input_list = []
    # src = src[178102:200000]
    src = src[:197559]
    for json_dict in tqdm(src):
        task_type = json_dict['task_type']
        que = json_dict['question']
        question = 'You are an expert in multimodal content understanding, particularly skilled in handling visual question answering tasks. Your task is: Given an image and a multimodal content understanding-related task label, along with a question related to that task label, the task label is “'+task_type+'”, the question is “'+que+'”, please fully understand the image content, the task label, and the question, and determine whether the task label and question are suitable for the image. If suitable, score it as 1; otherwise, score it as 0. Please only output your final score without any other characters.'
        image_path = json_dict["image_path"]
        input_list.append((image_path, question, json_dict))

    # print(len(input_list))
    # from concurrent.futures import ThreadPoolExecutor
    # executor = ThreadPoolExecutor(max_workers=30)
    # for inp in input_list:
        # executor.submit(glm4v_process, model, tokenizer, inp, output_file)
    for inp in tqdm(input_list):
        glm4v_process(model, tokenizer, inp, output_file)
    # print('Waiting for all subprocesses done...')
    # executor.shutdown(wait=True)
    # print('All subprocesses done.')
    


if __name__ == "__main__":
    device = "cuda:0"
    tokenizer = AutoTokenizer.from_pretrained("glm-4v-9b", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        "glm-4v-9b",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True
    ).to(device).eval()
    input_file = 'TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa_forfilter.json'
    run_caption(model, tokenizer, input_file, "TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa_forfilter_glm4v.json")