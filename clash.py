from method import generate_groups, format_file
import yaml
import argparse


# 命令行参数
parser = argparse.ArgumentParser(description="从代理列表和模板生成 Clash 配置")
parser.add_argument("--proxies", required=True, help="代理文件路径")
parser.add_argument("--template", required=True, help="模板文件路径")
parser.add_argument("--output", required=True, help="输出订阅文件路径")
args = parser.parse_args()

proxy_file = args.proxies
template_file = args.template
save_path = args.output

# 生成代理配置和代理组信息，用于替换模板中的占位符
proxy_config, proxy_groups = generate_groups(proxy_file)

# 读取模板，并填入代理配置和代理组信息
with open(template_file, 'r') as f:
    template = yaml.safe_load(f)
    template["proxies"] = proxy_config
    template["proxy-groups"] = proxy_groups

# 保存配置文件到指定路径
with open(save_path, 'w') as f:
    yaml.dump(template, f, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)

# 格式化配置文件
format_file(save_path)
