from urllib.parse import urlsplit
from base64 import b64decode
import json
import yaml


def url2config(proxy_url: str) -> dict:
    """
    将vmess的节点转换为clash配置
    """
    url = urlsplit(proxy_url)

    # 解析vmess链接
    if url.scheme == 'vmess':
        config = json.loads(b64decode(url.netloc).decode('utf-8'))
    else:
        return None

    # 根据解析的vmess链接生成clash配置
    clash_config = {
        'name': config['ps'],
        'server': config['add'],
        'port': config['port'],
        'type': 'vmess',
        'uuid': config['id'],
        'alterId': config['aid'],
        'cipher': 'auto' if config['type'] == 'none' else config['type'],
        'tls': True if config['tls'] == 'tls' else False,
        'network': config['net'],
        'skip-cert-verify': False,
        'udp': True
    }

    # 返回clash配置字符串和节点名称
    return clash_config


def generate_groups(proxy_file: str) -> tuple[list, list]:
    """
    读取代理组文件，生成代理配置和代理组配置
    """
    with open(proxy_file, 'r') as f:
        proxies_group = yaml.safe_load(f)

    config_list = []  # 用于保存代理配置
    group_list = []  # 用于保存代理组配置
    for group_name, proxies in proxies_group.items():
        # 遍历读取的代理组信息
        temp_group = {"name": group_name, "type": "select", "proxies": []}

        for proxy_url in proxies:
            # 遍历节点链接列表
            if proxy_url in ['DIRECT', 'REJECT', 'GLOBAL']:
                # 判断是否为特殊规则
                temp_group["proxies"].append(proxy_url)
            else:
                # 解析节点链接，生成代理和代理组配置
                clash_config = url2config(proxy_url)
                config_list.append(str(clash_config))  # clash_config转换为str存入代理配置
                temp_group["proxies"].append(clash_config["name"])

        group_list.append(temp_group)  # 保存代理组配置

    # 返回代理配置和代理组配置
    return config_list, group_list


def format_file(config_file):
    """
    格式化配置文件，删除所有的“'”
    """
    with open(config_file, 'r') as f:
        # 读取配置文件
        lines = f.readlines()

    format_lines = [line.replace("'", "") for line in lines]  # 删除所有的“'”

    with open(config_file, 'w') as f:
        # 保存格式化后的配置文件
        f.writelines(format_lines)
