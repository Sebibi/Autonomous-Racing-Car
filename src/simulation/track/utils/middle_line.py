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


def interpolate_line(line: np.ndarray, nb_points: int = 270):
    x = line[:, 0].astype(np.float64)
    y = line[:, 1].astype(np.float64)
    ind = np.arange(len(x))

    tck, u = splprep([ind, x, y], s=0)
    u_new = np.linspace(u.min(), u.max(), nb_points)
    new_line = splev(u_new, tck)
    new_line = np.array(new_line[1:]).T.astype(np.int32)
    return new_line


def get_track_center_line(image: np.ndarray, size: tuple[int, int], choice: int = 0, show: bool = False):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = image.T

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

    external = interpolate_line(external, 270)
    internal = interpolate_line(internal, 270)

    if show:
        temp_img = image.copy()
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_GRAY2RGB)
        for intern, extern in zip(internal, external):
            cv2.drawMarker(temp_img, tuple(intern), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)
            cv2.drawMarker(temp_img, tuple(extern), (0, 255, 0), cv2.MARKER_CROSS, 10, 2)
        cv2.imshow('Contours', temp_img)
        cv2.waitKey(0)

    center_line = get_centerline(internal, external)
    center_line2 = get_centerline(external, internal)
    center_line3 = get_centerline(center_line, center_line2)

    center_lines = [center_line3, center_line2, center_line]

    line = center_lines[0]
    new_line = interpolate_line(line, 270)
    new_points = scipy.ndimage.gaussian_filter1d(new_line, 1, axis=0, mode='nearest').astype(np.int32)
    contour_image = cv2.drawContours(contour_image, [new_points], 0, (255, 255, 255), 3)

    if show:
        cv2.imshow('Contours', contour_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    if True:
        track = np.zeros(shape=(len(new_points), 6))
        track[:, 0:2] = new_points
        track[:, 2:4] = internal
        track[:, 4:6] = external
        file_name = "map11.npy"
        np.save(os.path.dirname(__file__) + f"/../data_maps/{file_name}", track)
    return new_points


if __name__ == '__main__':
    image_input = cv2.imread(os.path.dirname(__file__) + "/../image_maps/map11.png")
    image_input = np.swapaxes(image_input, 0, 1)
    print(image_input.shape)
    center_line_track = get_track_center_line(image_input, (1600, 800), show=True)





