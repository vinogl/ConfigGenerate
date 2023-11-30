from urllib.parse import urlsplit
from base64 import b64encode, b64decode
import json
import yaml


def url2config(proxy_url):
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


def generate_groups(proxy_file):
    """
    读取代理组文件，生成代理配置和代理组配置
    """
    with open(proxy_file, 'r') as f:
        group_list = yaml.safe_load(f)

    proxy_config = []  # 用于保存代理配置
    proxy_group = []  # 用于保存代理组配置
    for group_name, proxies in group_list.items():
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
                # 将clash_config转换为str型，并删掉里面的所有'
                proxy_config.append(clash_config)
                temp_group["proxies"].append(clash_config["name"])

        proxy_group.append(temp_group)  # 保存代理组配置

    # 返回代理配置和代理组配置
    return proxy_config, proxy_group
