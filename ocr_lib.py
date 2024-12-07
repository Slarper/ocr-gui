from paddleocr import PaddleOCR

import numpy as np


def from_pil(im):
    '''
    from PIL.Image to ndarray
    '''
    return np.array(im)


def ocr(im, **kwargs):
    """
    im : ndarray or file_path

    PaddleOCR OCR API


    """
    ocr = PaddleOCR(
        use_angle_cls=True, **kwargs # lang="en" ; en, ch
    )  # need to run only once to download and load model into memory
    result = ocr.ocr(im, cls=True)  # image_array = np.array(image)
    return result


def text_only(result):
    '''
    Extract text from the output of PaddleOCR

    Warning: A paragraph will be separeted into multiple lines.
    '''

    # result will be [None] when there is no text detected in the image
    res = result[0] if result[0] is not None else []
    try:
        text_list = [line[1][0] for line in res]

    except Exception as e:
        print("Caught an error:", e)
        from pprint import pprint
        pprint(result)

    return text_list

def boxes_only(result):
    '''
    
    '''
    # result will be [None] when there is no text detected in the image
    res = result[0] if result[0] is not None else []

    try:
        boxes_list = [line[0] for line in res]

    except Exception as e:
        print("Caught an error:", e)
        from pprint import pprint
        pprint(result)

    return boxes_list


# test
if __name__ == "__main__":
    from PIL import Image
    from pprint import pprint

    im = Image.open("ppocr_img/imgs/11.jpg")
    pprint(ocr(from_pil(im)), indent=4)
    p = text_only(ocr(from_pil(im)))
    print(p)

def box_to_rect_ratio(box, max_width, max_height):
    """
    Convert a polygon defined by 4 vertices to a rectangle format.

    box : [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    Returns: (x, y, width, height)
    x, y, width, height are ratios
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

    return in_ratio
