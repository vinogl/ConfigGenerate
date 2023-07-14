from method import node2sub
import json
import os


# 读取文件路径
with open('Files/files_path.json', 'r') as f:
    file_info = json.load(f)

node_file = file_info["node_file"]  # 代理组文件路径
sub_filename = file_info["node_sub_filename"]  # 生成的配置文件名


# 获取保存路径
save_path = input('请输入保存路径(默认为当前路径): ')
if save_path == '':
    save_path = sub_filename  # 默认保存到当前路径
else:
    save_path = os.path.join(save_path, sub_filename)  # 保存到指定路径


# 生成订阅内容
node_sub = node2sub(node_file)


# 保存订阅内容到指定路径
with open(save_path, 'wb') as f:
    f.write(node_sub)
    print('保存成功')
