from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from PIL import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from ocr_lib import *
from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont("consolas", "Consolas.ttf"))
pdfmetrics.registerFont(TTFont("times_new_roman", "Times New Roman.ttf"))
pdfmetrics.registerFont(TTFont("jetbrainsmono", "JetBrainsMono-VariableFont_wght.ttf"))


def draw_page(im, c: canvas.Canvas):
    """
    im : image_file_path
    c : reportlab.pdfgen.canvas.Canvas
    Only support portrait A4 size
    """

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
        # c.rect(x, y, width, height, fill=0)  # Draw bounding box

        # Draw the text
        # 1 inch is roughly equal to 72 points.
        consolas_factor = 1.82
        times_new_roman_factor = 2.5
        jetbrainsmono_factor = 1.67
        font_size = width / len(txt) * jetbrainsmono_factor
        # Set the fill color with transparency (RGBA)
        c.setFillColor(colors.Color(1, 0, 0, 0.0))  # Red color with 50% transparency
        # c.setFillColor(colors.Color(1, 0, 0, 0.5))  # Debug
        c.setFont("jetbrainsmono", font_size)  # Set the font and size

        x_offset = 2.0
        y_offset = 1 * mm
        c.drawString(x + x_offset, y + y_offset, txt)  # Draw the text

        # frm = Frame(x, y, width, height, showBoundary=1,
        #             leftPadding = 0, rightPadding = 0, topPadding = 0, bottomPadding = 0)
        # txt_para = Paragraph(
        #     txt,
        #     ParagraphStyle(
        #         name="",
        #         fontName="consolas",
        #         fontSize=font_size,
        #         textColor="black",
        #         # alignment=TA_CENTER,
        #     ),
        # )
        # frm.addFromList([txt_para], c)

    c.showPage()


def calculate_font_size(width, height):
    """
    Calculate the font size based on the given width and height.
    This is a simple heuristic. You can adjust the scaling factors as needed.
    """
    # Use a scaling factor to calculate font size
    inch_to_pt = 72 / inch
    font_size = min(width * 2.0, height) * inch_to_pt
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
