from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm, mm

import os
image_folder = "lttctw_images"


from pdf_ocr_lib import *


c = canvas.Canvas("linear-types-can-change-the-world.ocr_fixed.pdf")
for image_file in os.listdir(image_folder):
    if image_file.endswith((".jpg", ".jpeg", ".png")):  # Check for image file types
        image_path = os.path.join(image_folder, image_file)
        print(image_path)
        draw_page(image_path, c)

c.save()
