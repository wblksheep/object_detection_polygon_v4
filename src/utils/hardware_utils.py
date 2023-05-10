import platform
import os

def get_hardware_acceleration():
    system = platform.system()
    if system == "Linux":
        if os.path.exists('/usr/local/cuda'):
            return "CUDA"
        elif os.path.exists('/opt/intel/openvino'):
            return "OpenVINO"
    elif system == "Windows":
        if os.path.exists('C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA'):
            return "CUDA"
        elif os.path.exists('C:\\Program Files (x86)\\IntelSWTools\\openvino'):
            return "OpenVINO"
    return "CPU"


if __name__ == "__main__":
    print(get_hardware_acceleration())
