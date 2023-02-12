import math


def find_location_idx(img_w, x_min, x_max):
    left_th = img_w // 3
    center_th = img_w * 2 // 3
    x_center = (x_min + x_max) // 2
    if x_center < left_th:
        return 0
    elif x_center < center_th:
        return 1
    else:
        return 2


def distance_degree(img_w, img_h, x_min, x_max, y_min, y_max):
    delta_x = (x_min + x_max) / 2 - img_w / 2
    delta_y = y_max - img_h
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    degree = int(-math.atan2(-delta_y, delta_x) * 180 / math.pi)
    return distance, degree


bbox = [1, 30, 1, 80]  # x_min, x_max, y_min, y_max
print(distance_degree(400, 200, *bbox))
