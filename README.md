# TaskGalaxy
[ICLR 2025] Scaling Multi-modal Instruction Fine-tuning with Tens of Thousands Vision Task Types

## Abstract
Multimodal visual language models are gaining prominence in open-world appli- cations, driven by advancements in model architectures, training techniques, and high-quality data. However, their performance is often limited by insufficient task- specific data, leading to poor generalization and biased outputs. Existing efforts to increase task diversity in fine-tuning datasets are hindered by the labor-intensive process of manual task labeling, which typically produces only a few hundred task types. To address this, we propose TaskGalaxy, a large-scale multimodal instruc- tion fine-tuning dataset comprising 19,227 hierarchical task types and 413,648 samples. TaskGalaxy utilizes GPT-4o to enrich task diversity by expanding from a small set of manually defined tasks, with CLIP and GPT-4o filtering those that best match open-source images, and generating relevant question-answer pairs. Multiple models are employed to ensure sample quality. This automated pro- cess enhances both task diversity and data quality, reducing manual interven- tion. Incorporating TaskGalaxy into LLaVA-v1.5 and InternVL-Chat-v1.0 models shows substantial performance improvements across 16 benchmarks, demonstrat- ing the critical importance of task diversity.

## Data Pipeline
![Alt text](/home/2022/jiankang/Storage/Mycode/TaskGalaxy/Pipeline/taskgalaxy_pipeline.png)

## Image Collection
