from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image
from ocr_lib import *

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont("consolas", "Consolas.ttf"))
pdfmetrics.registerFont(TTFont("times_new_roman", "Times New Roman.ttf"))
pdfmetrics.registerFont(TTFont("jetbrainsmono", "JetBrainsMono-VariableFont_wght.ttf"))
from reportlab.pdfbase.pdfmetrics import stringWidth


def draw_page(im, c: canvas.Canvas, **kargs):
    """
    im : image_file_path
    c : reportlab.pdfgen.canvas.Canvas
    Only support portrait A4 size
    """

    # if there is debug =True in kargs,
    debug_mode = kargs.get("debug", False)

    c.drawImage(im, 0, 0, 210 * mm, 297 * mm)

    result = ocr(im, lang="en")

    text = text_only(result)
    boxes = boxes_only(result)

    image = Image.open(im)  # Open the image to get dimensions
    img_width, img_height = image.size

    for box, txt in zip(boxes, text):
        x, y, width, height = box_to_rect_a4(
            box, img_width, img_height
        )  # Unpack box coordinates

        if debug_mode:
            c.rect(x, y, width, height, fill=0)  # Draw bounding box

        if not debug_mode:
            c.setFillColor(colors.Color(1, 0, 0, 0.0))
        else:
            c.setFillColor(colors.Color(1, 0, 0, 0.7))  # Debug
        font_size = adjust_font_size(txt, "times_new_roman", width)
        c.setFont("times_new_roman", font_size)  # Set the font and size


        # y + 1mm to centralize the txt vertically
        c.drawString(x, y + 1*mm, txt)  # Draw the text

    c.showPage()


def adjust_font_size(
    text,
    font_name,
    width,
):
    font_size = 18.0

    text_width = stringWidth(text, font_name, font_size)
    font_size = font_size * (width / text_width)
    return font_size


def box_to_rect_a4(box, max_width, max_height):
    """
    Convert a polygon defined by 4 vertices to a rectangle format.

    box : [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    Returns: (x, y, width, height)
    """

    # should flip y axis due to different coordinate system
    # between image and pdf
    x_coords = [point[0] for point in box]
    y_coords = [max_height - point[1] for point in box]

    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)

    width = x_max - x_min
    height = y_max - y_min

    in_ratio = (
        x_min / max_width,
        y_min / max_height,
        width / max_width,
        height / max_height,
    )

    a4_width = 210 * mm
    a4_height = 297 * mm

    in_a4 = (
        in_ratio[0] * a4_width,
        in_ratio[1] * a4_height,
        in_ratio[2] * a4_width,
        in_ratio[3] * a4_height,
    )

    return in_a4
