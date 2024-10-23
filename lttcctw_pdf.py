from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm, mm

c = canvas.Canvas("ex.pdf")
# c.drawImage("lttctw_images/page_001.jpg", 0, 0, 210 * mm, 297 * mm)
# c.showPage()
# c.save()

import os
image_folder = "lttctw_images"
# Loop through each file in the directory
# for image_file in os.listdir(image_folder):
#     if image_file.endswith((".jpg", ".jpeg", ".png")):  # Check for image file types
#         image_path = os.path.join(image_folder, image_file)
#         c.drawImage(image_path, 0, 0, 210 * mm, 297 * mm)  # Draw the image
#         c.showPage()  # Start a new page for the next image

from pdf_ocr_lib import *

# draw_page("lttctw_images/page_001.png",c)

for image_file in os.listdir(image_folder):
    if image_file.endswith((".jpg", ".jpeg", ".png")):  # Check for image file types
        image_path = os.path.join(image_folder, image_file)
        print(image_path)
        draw_page(image_path, c)

c.save()
