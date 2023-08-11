import cv2
import ctypes

# 创建一个窗口
cv2.namedWindow('My Window')

# 获取窗口的句柄
hwnd = cv2.getWindowProperty('My Window', cv2.WND_PROP_HWND)

# 将窗口设置为置顶
ctypes.windll.user32.SetWindowPos(int(hwnd), -1, 0, 0, 0, 0, 3)

# 展示图像
image = cv2.imread('image.jpg')
cv2.imshow('My Window', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
