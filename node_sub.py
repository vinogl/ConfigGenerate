from base64 import b64encode
import argparse


parser = argparse.ArgumentParser(description="从节点文件生成订阅")
parser.add_argument("--proxies", required=True, help="代理文件路径")
parser.add_argument("--output", required=True, help="输出订阅文件路径")
args = parser.parse_args()

node_file = args.proxies
save_path = args.output

# 读取节点文件，生成订阅内容
with open(node_file, 'rb') as file:
    content = file.read()  # 读取文件内容，二进制模式

node_sub = b64encode(content)  # 对内容进行Base64编码,得到订阅内容

# 保存订阅内容到指定路径
with open(save_path, 'wb') as f:
    f.write(node_sub)
