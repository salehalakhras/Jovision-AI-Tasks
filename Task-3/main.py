import numpy
import matplotlib.pyplot as plt
from PIL import Image
from os import listdir
from os.path import isfile, join
from openpyxl import Workbook
## all the fingers have the same length and width
## and the thumb is wider by 8 pixels from the other fingers
FINGER_LENGTH = 111
FINGER_WIDTH = 24


def extract_pressure_from_img(img_name):
    img = Image.open('images/' + img_name)
    # first extract only the pressure data
    color = img.getpixel((img.size[0] - 1, img.size[1] - 1));
    accepted = False
    # if it is green
    if color[1] > 200:
        accepted = True

    pressure_img = numpy.empty(dtype='uint8', shape=(int(img.size[0] / 2), img.size[1] - 9, 3))
    for row in range(img.size[1] - 9):
        for col in range(int(img.size[0] / 2)):
            pressure_img[col, row] = img.getpixel((col + 256, row))

    pressure_img = Image.fromarray(pressure_img)

    return [pressure_img, accepted]


def color_to_black(img):
    pixel_array = numpy.array(img)
    grey_pixel_array = numpy.empty(dtype='uint8', shape=(pixel_array.shape[0], pixel_array.shape[1]))
    for row in range(pixel_array.shape[0]):
        for col in range(pixel_array.shape[1]):
            red = pixel_array[row, col, 0]
            green = pixel_array[row, col, 1]
            blue = pixel_array[row, col, 2]
            grey = int(red * 0.3 + green * 0.59 + blue * 0.11)
            grey_pixel_array[row, col] = int(grey)
    grey_image = Image.fromarray(grey_pixel_array)

    return grey_image


def process_img(img):
    pixel_arr = numpy.array(img)

    for col in range(pixel_arr.shape[0]):
        for row in range(pixel_arr.shape[1]):
            if pixel_arr[col, row] < 29:  # the limit which outlines the hand data
                pixel_arr[col, row] = 0

    fingers_pos = [process_finger(pixel_arr, 0), process_finger(pixel_arr, 1), process_finger(pixel_arr, 2),
                   process_finger(pixel_arr, 3), process_finger(pixel_arr, 4)]

    palm_start = fingers_pos[4][1]
    palm_end = (pixel_arr.shape[0] - 1, 0)
    fingers_pos.append((palm_start, palm_end))

    return fingers_pos


## fingers are numbered from 0 to 4 with the thumb being 0 pinky 1 ring 2 and so on
def process_finger(img_arr, finger):
    start_position = (0, 0)
    if finger == 0:
        for col in range(0, img_arr.shape[0]):
            if img_arr[col, img_arr.shape[1] - 1] != 0:
                finger_start = (col, img_arr.shape[1] - 1)
                finger_end = (col + FINGER_WIDTH + 8, img_arr.shape[1] - 1 - FINGER_LENGTH)
                return finger_start, finger_end
    else:
        index = 0
        while index < img_arr.shape[1]:
            if img_arr[0, index] != 0:
                if finger == 1:
                    finger_start = (0, index)
                    finger_end = (FINGER_LENGTH, index + FINGER_WIDTH)
                    return finger_start, finger_end
                else:
                    finger -= 1
                    index = index + FINGER_WIDTH
            index += 1


def color_fingers(finger_data, arr):
    i = 0;
    img = numpy.array(arr)
    avg_arr = [];
    for finger in finger_data:
        average = numpy.int64(0)
        count = int(0)
        start_x = min(finger[0][0], finger[1][0])
        end_x = max(finger[0][0], finger[1][0])
        start_y = min(finger[0][1], finger[1][1]);
        end_y = max(finger[0][1], finger[1][1]);
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                count += 1
                average += img[x, y]
        i += 1
        avg_arr.append(average / count);

    return avg_arr

def save_to_excel(img_names, fingers_data):
    fingers = ["Thumb", "Pinky", "Ring", "Middle", "Index", "Palm"]
    wb = Workbook()
    ws = wb.active


img_files = [f for f in listdir("./images") if isfile(join("./images", f))]

finger_hold_threshold = [0, 0, 0, 0, 0, 0]
data = []
avg_arr = []
for img in img_files:
    [pressure_data_img, accepted] = extract_pressure_from_img(img)
    grey_img = color_to_black(pressure_data_img)
    finger_data = process_img(grey_img)
    avg = color_fingers(finger_data, grey_img)
    avg_arr.append(avg)
    for finger in range(6):
        if avg[finger] > finger_hold_threshold[finger] and not accepted:
            finger_hold_threshold[finger] = avg[finger]

i = 0
for img in img_files:
    fingers = [0, 0, 0, 0, 0, 0]
    for finger in range(6):
        if avg_arr[i][finger] > finger_hold_threshold[finger]:
            fingers[finger] = 1
    i += 1
    data.append(fingers)

for i in range(len(img_files)):
    print(img_files[i])
    print(data[i])

