from PIL import Image
import sys
import numpy


def color_to_black(img_name):
    img = Image.open(img_name)
    pixel_array = numpy.array(img)
    grey_pixel_array = numpy.empty(dtype='uint8', shape=(pixel_array.shape[0], pixel_array.shape[1]))
    for row in range(pixel_array.shape[0]):
        for col in range(pixel_array.shape[1]):
            red = pixel_array[row, col, 0]
            green = pixel_array[row, col, 1]
            blue = pixel_array[row, col, 2]
            grey = int(red * 0.3 + green * 0.59 + blue * 0.11)
            grey_pixel_array[row, col] = int(grey)
    print(grey_pixel_array.shape)
    grey_image = Image.fromarray(grey_pixel_array)
    grey_image.save('grey.png', color_type='')


if len(sys.argv) <= 1:
    print("Please provide an image name as an argument")
else:
    img_name = sys.argv[1]

    valid_image_ext = img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
    if valid_image_ext:
        color_to_black(img_name)
    else:
        print("Please enter a valid image")
