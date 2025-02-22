# TaskGalaxy
[ICLR 2025] Scaling Multi-modal Instruction Fine-tuning with Tens of Thousands Vision Task Types

## Abstract
Multimodal visual language models are gaining prominence in open-world appli- cations, driven by advancements in model architectures, training techniques, and high-quality data. However, their performance is often limited by insufficient task- specific data, leading to poor generalization and biased outputs. Existing efforts to increase task diversity in fine-tuning datasets are hindered by the labor-intensive process of manual task labeling, which typically produces only a few hundred task types. To address this, we propose TaskGalaxy, a large-scale multimodal instruc- tion fine-tuning dataset comprising 19,227 hierarchical task types and 413,648 samples. TaskGalaxy utilizes GPT-4o to enrich task diversity by expanding from a small set of manually defined tasks, with CLIP and GPT-4o filtering those that best match open-source images, and generating relevant question-answer pairs. Multiple models are employed to ensure sample quality. This automated pro- cess enhances both task diversity and data quality, reducing manual interven- tion. Incorporating TaskGalaxy into LLaVA-v1.5 and InternVL-Chat-v1.0 models shows substantial performance improvements across 16 benchmarks, demonstrat- ing the critical importance of task diversity.

## Data Pipeline
![Alt text](Pipeline/taskgalaxy_pipeline.png)

## Image Collection
### Images Download Links
#### MathV360K
- [MathV360K Dataset](https://huggingface.co/datasets/Zhiqiang007/MathV360K)
- Download: `data_images.zip`
- Path: `a_math_related/`

#### ALLAVA
- Main file contains the following download commands:
  - `download_laion.sh`
  - `download_vflan.sh`
- Downloaded paths:
  - `allava_laion/images`
  - `allava_vflan/images_vflan`

#### VG (Visual Genome)
- [VG_100K_2 Images (1)](https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip)
- [VG_100K_2 Images (2)](https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip)
- Download paths:
  - `a_visual_genome/VG_100K`
  - `a_visual_genome/VG_100K_2`

#### shareGPT4V
- Path: `a_sharegpt4v_data/coco_train2017`
  - [COCO 2017 Train Images](http://images.cocodataset.org/zips/train2017.zip)
- Additional datasets (download links available in the main file):
  - `a_sharegpt4v_data/sam_images`: [Link in `sam_images/sampath.sh`](https://ai.meta.com/datasets/segment-anything-downloads/)
  - For the following datasets, please refer to the [TaskGalaxy Dataset on Hugging Face](https://huggingface.co/datasets/CverCJK-huggingface/TaskGalaxy/):
    - `a_sharegpt4v_data/ocr_vqa_images`
    - `a_sharegpt4v_data/share_textvqa_images`
    - `a_sharegpt4v_data/text_vqa_train_images`
    - `a_sharegpt4v_data/web-celeberity_images`
    - `a_sharegpt4v_data/web-landmark_images`
    - `a_sharegpt4v_data/wikiart_images`
