from PIL import Image
import sys
import pytesseract

if len(sys.argv) <= 1:
    print("Please provide an image name as an argument")
else:
    img_name = sys.argv[1]

    valid_image_ext = img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
    if valid_image_ext:
        print(pytesseract.image_to_string(Image.open(img_name)))
    else:
        print("Please enter a valid image")
