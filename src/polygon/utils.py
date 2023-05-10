import cv2

def find_affected_curve(polygon, point):
    """
    根据给定的点，找到受影响的曲线
    :param polygon: 多边形实例
    :param point: 一个表示点的元组 (x, y)
    :return: 受影响的曲线的索引
    """
    for i, curve in enumerate(polygon.curves):
        if point in curve.points:
            return i
    return None

def update_polygon_area(polygon, curve_index, new_curve):
    """
    更新多边形区域，只更新受影响的部分
    :param polygon: 多边形实例
    :param curve_index: 需要更新的曲线的索引
    :param new_curve: 新的曲线实例
    """
    polygon.curves[curve_index] = new_curve
    polygon.calculate_area()
