import os
import numpy as np
import cv2

# map colour names to HSV ranges
color_list = [
    ['red', [0, 160, 70], [10, 250, 250]],
    ['pink', [0, 50, 70], [10, 160, 250]],
    ['yellow', [15, 50, 70], [30, 250, 250]],
    ['green', [40, 50, 70], [70, 250, 250]],
    ['cyan', [80, 50, 70], [90, 250, 250]],
    ['blue', [100, 50, 70], [130, 250, 250]],
    ['purple', [140, 50, 70], [160, 250, 250]],
    ['red', [170, 160, 70], [180, 250, 250]],
    ['pink', [170, 50, 70], [180, 160, 250]]
]


def detect_object_color(file_name):
    img = cv2.imread(file_name)
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    color_found = 'undefined'
    max_count = 0

    for color_name, lower_val, upper_val in color_list:
        # threshold the HSV image - any matching color will show up as white
        mask = cv2.inRange(hsv_image, np.array(lower_val), np.array(upper_val))

        # count white pixels on mask
        count = np.sum(mask)
        if count > max_count:
            color_found = color_name
            max_count = count

    return color_found


def detect_object_position(img_path, show_window):

    img_original = cv2.imread(img_path)
    img_resized = cv2.resize(img_original, (400, 500))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    _, img_theshold = cv2.threshold(img_gray, 100, 255, 0)
    # mask = np.zeros(img_theshold.shape, np.uint8)
    contours, _ = cv2.findContours(
        img_theshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    centerX, centerY = -1, -1
    for cnt in contours:
        if 1000 < cv2.contourArea(cnt) < 10000:
            # cv2.drawContours(img_resized, [cnt], 0, (0, 255, 0), 2)
            # cv2.drawContours(mask, [cnt], 0, 255, -1)
            (x, y, w, h) = cv2.boundingRect(cnt)
            break

    if w > h:
        col = img_theshold[:, x + int(w / 2)]
        black_pixels = np.where(col == 0)[0]
        if len(black_pixels) > 0:
            first_black_pixel_y = black_pixels[0]
            last_black_pixel_y = black_pixels[-1]
            if show_window:
                cv2.circle(img_theshold, (x + int(w / 2),
                                          first_black_pixel_y), 5, 0, 3)
                cv2.circle(img_theshold, (x + int(w / 2),
                                          last_black_pixel_y), 5, 0, 3)
            centerX, centerY = x + \
                int(w / 2), int((first_black_pixel_y + last_black_pixel_y) / 2)
    else:
        row = img_theshold[y + int(h / 2), :]
        black_pixels = np.where(row == 0)[0]
        if len(black_pixels) > 0:
            first_black_pixel_x = black_pixels[0]
            last_black_pixel_x = black_pixels[-1]
            if show_window:
                cv2.circle(img_theshold, (first_black_pixel_x,
                           y + int(h / 2)), 5, 0, 3)
                cv2.circle(img_theshold, (last_black_pixel_x,
                           y + int(h / 2)), 5, 0, 3)
            centerX, centerY = int(
                (first_black_pixel_x + last_black_pixel_x) / 2), y + int(h / 2)

    if show_window:
        cv2.rectangle(img_theshold, (x, y), (x+w, y+h), 0, 2)
        cv2.circle(img_theshold, (centerX, centerY), 8, 255, -1)
        cv2.imshow("Test", img_theshold)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return centerX, centerY, x, y, w, h

'''
file_name = "image.jpg"
print(f"{file_name}: {detect_object_color(file_name)}")
centerX, centerY, x, y, w, h = detect_object_position(file_name, True)
print(f"Center: ({centerX}, {centerY})")
print(f"Position: ({x}, {y})")
print(f"Width x height: {w} x {h}")
'''

