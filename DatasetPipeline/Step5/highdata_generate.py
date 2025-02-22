# 将几个裁判模型的打分汇总
from tqdm import tqdm
import json
def find_same_data(source_data, target_data, target_data_2, result_file):
    flag = False
    for data in target_data:
        if data['image_path'] == source_data['image_path'] and data['task_type'] == source_data['task_type']:
            for data_2 in target_data_2:
                if data_2['image_path'] == source_data['image_path'] and data_2['task_type'] == source_data['task_type']:
                    item = {}
                    item['image_path'] = source_data['image_path']
                    item['task_type'] = source_data['task_type']
                    item['question'] = source_data['question']
                    item['answer'] = source_data['answer']
                    item['intervl2_26B_score'] = source_data['model_output']
                    item['glm4v_score'] = data['model_output']
                    item['intervl_score'] = data_2['model_output']
                    with open(result_file, 'a') as f:
                        f.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
                        f.flush()
                        flag = True
                    break
        if flag == True:
            break
        
# 获取分数总和大于等于2的数据
def high_quality_data(file_list, result_file):
    intervl2_26B_data = []
    glm4v_data = []
    intervl_data = []
    
    # intervl2_26B
    file = file_list[0]
    lines = open(file, 'r')
    for line in lines:
        try:
            intervl2_26B_data.append(json.loads(line))
        except:
            continue
    
    # glm4v
    file = file_list[1]
    lines = open(file, 'r')
    for line in lines:
        try:
            glm4v_data.append(json.loads(line))
        except:
            continue

    # internVL
    file = file_list[2]
    lines = open(file, 'r')
    for line in lines:
        try:
            intervl_data.append(json.loads(line))
        except:
            continue
    for data in tqdm(intervl2_26B_data):
        find_same_data(data, glm4v_data, intervl_data, result_file)

# 投票决定最终生成wtaskdataset的数据
def wtaskdatasetgeneration(score_all_file, wtaskdataset):
    json_data = []
    file = open(score_all_file, 'r')
    for line in file:
        try:
            json_data.append(json.loads(line))
        except:
            continue
    output_file = open(wtaskdataset, 'a')
    for data in json_data:
        item = {}
        item['image_path'] = data['image_path']
        item['task_type'] = data['task_type']
        item['question'] = data['question']
        item['answer'] = data['answer']
        intervl2_26B_score = data['intervl2_26B_score']
        glm4v_score = data['glm4v_score']
        intervl_score = data['intervl_score']
        try:
            score = int(intervl2_26B_score) + int(glm4v_score) +int(intervl_score)
            if score>=2:
                output_file.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
                output_file.flush()
        except:
            continue


if __name__ == '__main__':
    file_list = ['TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa_forfilter_internvl2_26B.json','TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa_forfilter_glm4v.json', 'TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_4o_qa_forfilter_internvl.json']
    result_file = 'TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset_allscore.json'
    high_quality_data(file_list, result_file)
    wtaskdatafile = 'TaskGalaxy/DatasetPipeline/taskgalaxy_.json'
    wtaskdatasetgeneration(result_file, wtaskdatafile)

        