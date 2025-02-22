

# laion_root="allava_laion"

# mkdir $laion_root
# cd $laion_root


# # 1. download annotation files 
# ## 1.1 caption
# wget -c -O ALLaVA-Caption-LAION-4V.json https://huggingface.co/datasets/FreedomIntelligence/ALLaVA-4V/resolve/main/allava_laion/ALLaVA-Caption-LAION-4V.json?download=true

# ## 1.2 instruction
# wget -c -O ALLaVA-Instruct-LAION-4V.json https://huggingface.co/datasets/FreedomIntelligence/ALLaVA-4V/resolve/main/allava_laion/ALLaVA-Instruct-LAION-4V.json?download=true


# # 2. download and upzip images
# mkdir image_chunks

## 2.1 download
# for i in 1 2 3 4 5 6 7 8 9
# do
#     wget -c -O /mllm_hdd/chenjiankang/research_dataset/ALLaVA/allava_laion/image_chunks/images_$i.zip https://huggingface.co/datasets/FreedomIntelligence/ALLaVA-4V/resolve/main/allava_laion/image_chunks/images_$i.zip?download=true &
# done

## 2.2 unzip 
for i in 0 1 2 3 4 5 6 7 8 9
do
    unzip -j /mllm_hdd/chenjiankang/research_dataset/ALLaVA/allava_laion/image_chunks/images_$i.zip -d images/ & # wait patiently, it takes a while...
done

# for ((i=1; i<3; i++))
# do
#     unzip -j i$i.zip -d i/ & # wait patiently, it takes a while...
# done
# unzip -j /mllm_hdd/chenjiankang/research_dataset/MathV360K/data_images.zip -d /mllm_hdd/chenjiankang/research_dataset/MathV360K