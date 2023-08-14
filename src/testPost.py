import json

import requests

# 创建一个会话对象
session = requests.Session()

# 定义登录URL和凭据
login_url = "http://zns.china-yd.com:20001/user/login"
headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
}
credentials = {
    "code": "hello123456",
    "userName": "admin",
    "verifyType": "verifyPassword"
}

# 发送登录请求
login_response = session.post(login_url, data=credentials)

# 打印所有响应头
print(login_response.headers)

# 打印响应体
print(login_response.text)
# 检查登录是否成功
if login_response.status_code == 200:
    url = 'http://zns.china-yd.com:20001/monitor/getHKMonitorUrl'
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'sessionId=e56668e2-851f-49a8-98dc-70d7fa5eb9df',
        'Accept': 'application/json',
    }
    data = {
      "brokerId": 2,
      "cameraIndexCode": "000649a9fa9847a69348dc4b15f1532f",
      "protocol": "rtmp",
      "streamType": 0,
      "transmode": 1
    }
    response = session.post(url, json=data, headers=headers)
    res = json.loads(response.text)
    # 打印受保护资源的内容
    print(response.text)
else:
    print("登录失败")

# 关闭会话
session.close()
