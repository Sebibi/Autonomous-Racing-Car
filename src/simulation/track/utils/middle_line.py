import os.path
import random

import cv2
import numpy as np
import scipy.interpolate
from scipy import interpolate
from scipy.interpolate import splev, splprep


def get_closest_point(center: np.ndarray, line: np.ndarray):
    distances = np.linalg.norm(line - center, axis=1)
    closest_arg = np.argmin(distances)
    return line[closest_arg]


def get_centerline(line1: np.ndarray, line2: np.ndarray):
    center_line = []
    for i in range(len(line1)):
        closest_point = get_closest_point(line1[i], line2)
        center_line.append((line1[i] + closest_point) / 2)
    return np.array(center_line, dtype=np.int32)


def get_track_center_line(image_path: str, size: tuple[int, int], choice: int = 0, show: bool = False):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, size)
    image_bin = (image > 128).astype(np.uint8)

    contours, res = cv2.findContours(image_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=len, reverse=True)

    contour_image = image.copy()
    contour_image = cv2.cvtColor(contour_image, cv2.COLOR_GRAY2RGB)
    contour_image = cv2.drawContours(contour_image, sorted_contours, 0, (0, 0, 255), 3)
    contour_image = cv2.drawContours(contour_image, sorted_contours, 1, (0, 0, 255), 3)

    external = np.array(sorted_contours[0], dtype=np.int32).reshape(-1, 2)
    internal = np.array(sorted_contours[1], dtype=np.int32).reshape(-1, 2)

    center_line = get_centerline(internal, external)
    center_line2 = get_centerline(external, internal)
    center_line3 = get_centerline(center_line, center_line2)

    center_lines = [center_line3, center_line2, center_line]

    line = center_lines[choice]
    x = line[:, 0].astype(np.float64)
    y = line[:, 1].astype(np.float64)
    ind = np.arange(len(x))

    tck, u = splprep([ind, x, y], s=0)
    u_new = np.linspace(u.min(), u.max(), 270)
    new_points = splev(u_new, tck)
    new_points = np.array(new_points[1:]).T.astype(np.int32)
    new_points = scipy.ndimage.gaussian_filter1d(new_points, 1, axis=0, mode='nearest').astype(np.int32)
    contour_image = cv2.drawContours(contour_image, [new_points], 0, (255, 255, 255), 3)

    if show:
        cv2.imshow('Contours', contour_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return new_points


if __name__ == '__main__':
    line = get_track_center_line(os.path.dirname(__file__) + "/../image_maps/map2.png", (1600, 800))



