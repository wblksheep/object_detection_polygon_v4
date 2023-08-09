import cv2
import torch
from ultralytics.utils.checks import is_ascii


class MyAnnotator:
    def __init__(self, annotator):
        self.annotator = annotator

    def box_label(self, box, label='', color=(128, 128, 128), txt_color=(255, 255, 255)):
        """Add one xyxy box to image with label."""
        if isinstance(box, torch.Tensor):
            box = box.tolist()
        if self.annotator.pil or not is_ascii(label):
            self.annotator.draw.rectangle(box, width=self.annotator.lw, outline=color)  # box
            if label:
                w, h = self.annotator.font.getsize(label)  # text width, height
                outside = box[1] - h >= 0  # label fits outside box
                self.annotator.draw.rectangle(
                    (box[0], box[1] - h if outside else box[1], box[0] + w + 1,
                     box[1] + 1 if outside else box[1] + h + 1),
                    fill=color,
                )
                # self.draw.text((box[0], box[1]), label, fill=txt_color, font=self.font, anchor='ls')  # for PIL>8.0
                self.annotator.draw.text((box[0], box[1] - h if outside else box[1]), label, fill=txt_color, font=self.annotator.font)
        else:  # cv2
            p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
            cv2.rectangle(self.annotator.im, p1, p2, color, thickness=self.annotator.lw, lineType=cv2.LINE_AA)
            x, y = int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)
            # 在图像上添加坐标文本
            coordinate_text = f"({x}, {y})"
            cv2.putText(self.annotator.im, coordinate_text, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
            # 绘制一条从坐标原点到随机点的线
            cv2.line(self.annotator.im, (0, 0), (x, y), color=(0, 255, 0), thickness=2)
            if label:
                tf = max(self.annotator.lw - 1, 1)  # font thickness
                w, h = cv2.getTextSize(label, 0, fontScale=self.annotator.lw / 3, thickness=tf)[0]  # text width, height
                outside = p1[1] - h >= 3
                p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
                # cv2.rectangle(self.annotator.im, p1, p2, color, -1, cv2.LINE_AA)  # filled
                # cv2.putText(self.annotator.im,
                #             label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                #             0,
                #             self.annotator.lw / 3,
                #             txt_color,
                #             thickness=tf,
                #             lineType=cv2.LINE_AA)

