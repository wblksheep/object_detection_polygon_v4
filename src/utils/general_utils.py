import yaml

def load_config(file_path):
    """
    加载配置文件
    :param file_path: 配置文件路径
    :return: 配置文件的字典
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
