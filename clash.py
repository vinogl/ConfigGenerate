from method import generate_groups
import json
import yaml
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

# 读取模板，并填入代理配置和代理组信息
with open(template_file, 'r') as f:
    template = yaml.safe_load(f)
    template["proxies"] = proxy_config
    template["proxy-groups"] = proxy_groups

# 保存配置文件到指定路径
with open(save_path, 'w') as f:
    yaml.dump(template, f, sort_keys=False, allow_unicode=True, default_flow_style=False)
