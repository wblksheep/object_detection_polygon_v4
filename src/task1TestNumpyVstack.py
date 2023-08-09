import numpy as np

arr = np.array([[1, 2], [3, 4]])
new_row = np.array([[5, 6]])

# 沿第一个轴（行）添加新的行
arr = np.vstack((arr, new_row))

print(arr)
# 输出
# [[1 2]
#  [3 4]
#  [5 6]]
