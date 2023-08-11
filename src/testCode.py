import numpy as np
from matplotlib import pyplot as plt

mask = np.load('display1_mask.npy')
# 使用matplotlib将NumPy数组显示为灰度图像
plt.imshow(mask, cmap='gray')
# 保存图像
plt.savefig('now_mask.png', bbox_inches='tight', pad_inches=0)
x = 330
y = 329
print(mask[y, x] == 255)
