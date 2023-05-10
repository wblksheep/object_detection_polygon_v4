import os
import yaml

def get_project_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    return project_root

def load_config():
    # 读取config.yaml文件内容
    with open(os.path.join(get_project_root(), "configs/config.yaml"), "r") as file:
        config_data = yaml.safe_load(file)

    # 获取资源目录的相对路径
    resources_path_relative = config_data["resources_path"]

    # 获取项目根目录和资源目录的绝对路径
    PROJECT_ROOT_PATH = get_project_root()
    RESOURCES_PATH = os.path.join(PROJECT_ROOT_PATH, resources_path_relative)

    return PROJECT_ROOT_PATH, RESOURCES_PATH
