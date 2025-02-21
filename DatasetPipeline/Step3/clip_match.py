import torch 
from PIL import Image
from tqdm import tqdm
import os
import json
import ssl
import clip
import numpy as np
import torch.nn.functional as F
import datasets

def top_k_indices_and_values(lst, k): #返回列表中的前k大的值及其索引
    # 使用 heapq.nlargest 找到前 k 大的元素及其索引
    top_k = heapq.nlargest(k, enumerate(lst), key=lambda x: x[1])
    # 将结果分解为索引和值
    indices, values = zip(*top_k)
    return list(indices), list(values)


device = "cuda:0" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
# model, preprocess = load_from_name()
model.eval()



output_file_image_task_type = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_related_dataset.json','w')
task_embedding = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_embedding.json','w')

task_file = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_all.txt', 'r')#所有任务类型
tasks = task_file.read().splitlines()
将所有的task_type通过clip的text_encoder得到相应的embedding保存在json文件中
for task in tqdm(tasks):
    text = clip.tokenize(task).to(device)
    text_feature = model.encode_text(text)
    item = {}
    item['task_type'] = task
    item['embedding'] = text_feature.detach().cpu().numpy().tolist()
    task_embedding.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
    task_embedding.flush()


all_image_path = os.listdir('TaskGalaxy/DatasetPipeline/Step3/Dataset/images')#列出所有图像路径
Image_path = []
for image_path in all_image_path:
    if '.py' in image_path or '.json' in image_path:
        continue
    Image_path.append(image_path)
# print(Image_path)

#获取所有文本的embedding
task_embedding = open('TaskGalaxy/DatasetPipeline/Step3/Dataset/task_embedding.json','r')
task_data = []
task_type = []
for line in task_embedding:
    task_type.append(json.loads(line)['task_type'])
    task_data.append(np.array(json.loads(line)['embedding']))

task_data = np.array(task_data)
task_data = torch.from_numpy(task_data).float().to('cuda:0')
for each_image_folder in tqdm(Image_path):##视图像数据集的目录形式[有多少级]而定
    each_all_image_path = os.listdir(os.path.join('TaskGalaxy/DatasetPipeline/Step3/Dataset/images', each_image_folder))
    for image_pa in tqdm(each_all_image_path):
        image_path = os.path.join('TaskGalaxy/DatasetPipeline/Step3/Dataset/images',each_image_folder,image_pa)
        try:
            # image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        except:
            continue
        with torch.no_grad():
            #得到该图像特征 
            image_feature = model.encode_image(image).float()
            # image_featrue = model.encode_image(image).float()
            image_feature = F.normalize(image_feature, dim=1)
            text_feature = F.normalize(task_data.squeeze().T, dim=1) #将double类型转位float32计算相似度
            
            # print(text_feature.shape)
            similarity = image_feature @ text_feature #得到给图像特征与相应task_type的相似度
            # print(similarity.shape)
            k = 5#每张图片找前5大相似度对应的任务类型
            topk_values, topk_indices = torch.topk(similarity, k) #选择和该图像最相似的task_type
            item = {}
            item["image_path"] = image_path
            indices = np.array(topk_indices.squeeze().cpu()).tolist()
            t_type = []
            for ind in indices:
                t_type.append(tasks[ind])
            item["related_task_type"] = t_type
            item["score"] = np.array(topk_values.squeeze().cpu()).tolist()
            output_file_image_task_type.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))
            output_file_image_task_type.flush()
# text_feature = F.normalize(task_data.squeeze().T, dim=1) #将double类型专为float32机型计算相似度