import os

def get_directory_tree(root_dir):
    tree = []
    for root, dirs, files in os.walk(root_dir):
        # 只选择没有子目录的目录，即叶子目录
        if not dirs:
            rel_path = os.path.relpath(root, root_dir)
            tree.append(rel_path.replace(os.sep, '~'))
    return tree

root_directory = 'TaskGalaxy/DatasetPipeline/Step1/Tasktype'  # 替换为你的根目录路径
directory_tree = get_directory_tree(root_directory)
print(len(directory_tree))
# 写入到文件
with open('TaskGalaxy/DatasetPipeline/Step1/tasktype.txt', 'w') as f:
    for path in directory_tree:
        f.write(path + '\n')