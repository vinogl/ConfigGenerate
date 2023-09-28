from method import generate_groups
import json
import os


# 读取文件路径
with open('Files/files_path.json', 'r') as f:
    file_info = json.load(f)

proxy_file = file_info["clash_proxies"]  # 代理组文件路径
template_file = file_info["clash_config_template"]  # 模板文件路径
config_filename = file_info["clash_config_filename"]  # 生成的配置文件名
save_path = os.path.join(file_info["save_path"], config_filename)  # 生成配置文件的保存路径


# 生成代理配置和代理组信息，用于替换模板中的占位符
proxy_config, proxy_groups = generate_groups(proxy_file)


# 读取模板，并替换占位符
with open(template_file, 'r') as f:
    template = f.read()
    template = template.replace('  $$PROXY_CONFIG$$', proxy_config.strip('\n'))
    template = template.replace('  $$PROXY_GROUPS$$', proxy_groups.strip('\n'))


# 保存配置文件到指定路径
with open(save_path, 'w') as f:
    f.write(template)
