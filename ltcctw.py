

from pdf2image import convert_from_path
from PIL import Image

# Convert PDF to images
images = convert_from_path("linear-type-can-change-the-world.pdf",dpi=600)
save_path = "lttctw_images/"
index = 1

import os
for image in images:
    width, height = image.size

    # Define boxes for left and right halves
    left_box = (0, 0, width // 2, height)
    right_box = (width // 2, 0, width, height)

    # Crop and save left half
    left_image = image.crop(left_box)
    left_image.save(os.path.join(save_path,f"page_{index:03}.png"), "PNG")

    # Crop and save right half
    right_image = image.crop(right_box)
    right_image.save(os.path.join(save_path,f"page_{index + 1:03}.png"), "PNG")

    index += 2  # Increment by 2 for the next pair

