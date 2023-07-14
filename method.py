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
        'skip-cert-verify': 'false',
        'udp': 'true'
    }

    # 将clash配置转换为字符串
    config_str = '- { '
    for key, value in clash_config.items():
        if key == list(clash_config.keys())[-1]:
            config_str += '%s: %s' % (key, value)
        else:
            config_str += '%s: %s, ' % (key, value)
    config_str += ' }'

    # 返回clash配置字符串和节点名称
    return config_str, clash_config['name']


def generate_groups(proxy_file):
    """
    生成代理配置和代理组，用于替换模板(clash_template.yaml)中的占位符
    """
    with open(proxy_file, 'r') as f:
        group_list = yaml.safe_load(f)

    proxy_config = ''  # 用于保存代理配置
    proxy_group = ''  # 用于保存代理组配置
    for group_name, proxies in group_list.items():
        # 遍历读取的代理组信息
        proxy_group += \
            '\n' \
            '  - name: %s\n' \
            '    type: select\n' \
            '    proxies:\n' % group_name

        for proxy_url in proxies:
            # 遍历节点链接列表
            if proxy_url in ['DIRECT', 'REJECT', 'GLOBAL']:
                # 判断是否为特殊规则
                proxy_group += '      - %s\n' % proxy_url
            else:
                # 解析节点链接，生成代理配置和代理组配置
                config, name = url2config(proxy_url)
                proxy_config += '  %s\n' % config
                proxy_group += '      - %s\n' % name

    # 返回代理配置和代理组配置
    return proxy_config, proxy_group


def node2sub(node_file):
    """
    读取节点文件，生成订阅内容
    """
    with open(node_file, 'rb') as file:
        content = file.read()  # 读取文件内容，二进制模式

    sub_content = b64encode(content)  # 对内容进行Base64编码,得到订阅内容
    return sub_content
