import yaml
import os
from base64 import b64encode

# 读取文件路径
with open('Files/files_path.yaml', 'r') as f:
    file_info = yaml.safe_load(f)

node_file = file_info["node_file"]  # 代理组文件路径
sub_filename = file_info["node_sub_filename"]  # 生成的配置文件名
save_path = os.path.join(file_info["save_path"], sub_filename)  # 生成配置文件的保存路径

# 读取节点文件，生成订阅内容
with open(node_file, 'rb') as file:
    content = file.read()  # 读取文件内容，二进制模式

node_sub = b64encode(content)  # 对内容进行Base64编码,得到订阅内容

# 保存订阅内容到指定路径
with open(save_path, 'wb') as f:
    f.write(node_sub)
