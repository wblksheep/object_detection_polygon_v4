import numpy as np
ret_points = np.array([[299, 332], [822, 333]], dtype=np.float32)
points = ret_points.tolist() if ret_points is not None else ""
print(points)

# import numpy as np
# import json
#
# # 创建一个二维NumPy数组
# numpy_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#
# # 将NumPy数组转化为Python列表
# python_list = numpy_array.tolist()
#
# # 将列表转化为JSON字符串
# json_str = json.dumps(python_list)
#
# # 打印JSON字符串
# print(json_str)  # 输出：[[1, 2, 3], [4, 5, 6], [7, 8, 9]]

