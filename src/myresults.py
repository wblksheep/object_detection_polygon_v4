from copy import deepcopy

import cv2
import numpy as np
import torch
from matplotlib import pyplot as plt
from ultralytics.data.augment import LetterBox
from ultralytics.utils.plotting import Annotator, colors

from src.myannotator import MyAnnotator


class MyResults:
    def __init__(self, results, name):
        self.results = results
        self.name = name

    def plot(self,
             conf=True,
             line_width=None,
             font_size=None,
             font='Arial.ttf',
             pil=False,
             img=None,
             im_gpu=None,
             kpt_radius=5,
             kpt_line=True,
             labels=True,
             boxes=True,
             masks=True,
             probs=True,
             rect_width=300,
             rect_height=200,
             image_shape=(1440, 2560),
             origin=(0, 0),
             **kwargs  # deprecated args TODO: remove support in 8.2
             ):
        if img is None and isinstance(self.results.orig_img, torch.Tensor):
            img = np.ascontiguousarray(self.results.orig_img[0].permute(1, 2, 0).cpu().detach().numpy()) * 255

        names = self.results.names
        pred_boxes, show_boxes = self.results.boxes, boxes
        pred_masks, show_masks = self.results.masks, masks
        pred_probs, show_probs = self.results.probs, probs
        annotator = Annotator(
            deepcopy(self.results.orig_img if img is None else img),
            line_width,
            font_size,
            font,
            pil or (pred_probs is not None and show_probs),  # Classify tasks default to pil=True
            example=names)
        my_annotator = MyAnnotator(annotator)

        # Plot Segment results
        if pred_masks and show_masks:
            if im_gpu is None:
                img = LetterBox(pred_masks.shape[1:])(image=annotator.result())
                im_gpu = torch.as_tensor(img, dtype=torch.float16, device=pred_masks.data.device).permute(
                    2, 0, 1).flip(0).contiguous() / 255
            idx = pred_boxes.cls if pred_boxes else range(len(pred_masks))
            my_annotator.annotator.masks(pred_masks.data, colors=[colors(x, True) for x in idx], im_gpu=im_gpu)
        my_mask = np.load(f"{self.name}_mask.npy")
        first_mat = np.load(f"{self.name}_first_mat.npy")
        second_mat = np.load(f"{self.name}_second_mat.npy")
        ret_points = None
        # Plot Detect results
        if pred_boxes and show_boxes:
            points = []
            for d in reversed(pred_boxes):
                # print(d.boxes)
                x1, y1, x2, y2 = d.xyxy.squeeze()
                x, y = int((x1 + x2)/2), int((y1 + y2)/2)
                if my_mask[y, x] == 255:
                    points.append([x, image_shape[0] - 1 - y])
                c, conf, id = int(d.cls), float(d.conf) if conf else None, None if d.id is None else int(d.id.item())
                name = ('' if id is None else f'id:{id} ') + names[c]
                label = (f'{name} {conf:.2f}' if conf else name) if labels else None
                my_annotator.box_label(d.xyxy.squeeze(), label, color=colors(c, True))
            if points:
                points = np.asarray(points, dtype=np.float32)
                # points = np.asarray([[1629, 517]], dtype=np.float32)
                p_points = np.array([
            [
                544.0,
                464.0
            ],
            [
                563.0,
                983.0
            ],
            [
                2502.0,
                841.0
            ],
            [
                2382.0,
                186.99999999999994
            ]
        ], dtype=np.float32)
                # 将点转换为齐次坐标
                points_homogeneous = np.column_stack((p_points, np.ones(p_points.shape[0])))
                # 应用单应性矩阵
                transformed_points_homogeneous = np.dot(first_mat, points_homogeneous.T).T
                transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
                transformed_points = transformed_points.astype(np.int32)
                points = np.vstack((points, transformed_points))
                # 将点转换为齐次坐标
                points_homogeneous = np.column_stack((points, np.ones(points.shape[0])))
                # 应用单应性矩阵
                transformed_points_homogeneous = np.dot(second_mat, points_homogeneous.T).T
                transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
                transformed_points = transformed_points.astype(np.int32)
                ret_points = np.array(transformed_points, dtype=np.float32)
                ret_points[:, 1] = rect_height-ret_points[:, 1]
                # 可视化原始点和变换后的点
                plt.figure(figsize=(10, 6))

                plt.plot(points[:, 0], points[:, 1], 'bo', label='Original Points')
                plt.plot(transformed_points[:, 0], transformed_points[:, 1], 'ro', label='Transformed Points')

                for i in range(points.shape[0]):
                    plt.plot([points[i, 0], transformed_points[i, 0]], [points[i, 1], transformed_points[i, 1]], 'g-')

                plt.legend()
                plt.title('Visualization of Points Transformed by Homography Matrix')
                plt.axis('equal')
                plt.show()
                # 创建一个200*300的空白图像
                screen = np.zeros((rect_height, rect_width, 3), dtype="uint8")
                # 定义点的大小
                radius = 5
                # 显示图像
                for point in transformed_points:
                    cv2.circle(screen, (point[0], rect_height-point[1]), radius, (0, 255, 0), -1)

                cv2.imshow(self.name, screen)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            else:
                # 创建一个200*300的空白图像
                screen = np.zeros((rect_height, rect_width, 3), dtype="uint8")
                cv2.imshow(self.name, screen)
        else:
            # 创建一个200*300的空白图像
            screen = np.zeros((rect_height, rect_width, 3), dtype="uint8")
            cv2.imshow(self.name, screen)

        # Plot Classify results
        if pred_probs is not None and show_probs:
            text = ',\n'.join(f'{names[j] if names else j} {pred_probs.data[j]:.2f}' for j in pred_probs.top5)
            x = round(self.results.orig_shape[0] * 0.03)
            my_annotator.annotator.text([x, x], text, txt_color=(255, 255, 255))  # TODO: allow setting colors

        # Plot Pose results
        if self.results.keypoints is not None:
            for k in reversed(self.results.keypoints.data):
                my_annotator.annotator.kpts(k, self.results.orig_shape, radius=kpt_radius, kpt_line=kpt_line)

        return my_annotator.annotator.result(), ret_points

    def __getattr__(self, attr):
        # this method is called when the requested attribute is not found in the class
        # we will try to get it from the Results object
        return getattr(self.results, attr)
