import svgwrite
import base64
from PIL import Image


def get_image_size(file_path):
    with Image.open(file_path) as img:
        return img.size  # returns (width, height)


image_path = "general_ocr_002.png"

output_file = image_path + ".svg"
# Example usage
width, height = get_image_size(image_path)

dwg = svgwrite.Drawing(output_file, size=(str(width) + "px", str(height) + "px"))


# Embed image as base64
def embed_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/{image_path.split('.')[-1]};base64,{encoded}"


# Add embedded image
dwg.add(dwg.image(href=embed_image(image_path), insert=(0, 0), size=(width, height)))


json_path = "output/general_ocr_002_res.json"

import json

# Read JSON from a file
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

text_list = data["rec_texts"]

pos_list = data["rec_boxes"]

pos_list = [(x[0], x[1]) for x in pos_list]

for i in range(len(pos_list)):

    dwg.add(
        dwg.text(
            text_list[i],
            insert=pos_list[i],
            font_size=f"{10}px",
            font_weight="normal",
            fill="red",
        )
    )

dwg.save()
