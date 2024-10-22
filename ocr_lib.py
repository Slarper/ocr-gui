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
    res = result[0]
    text_list = [line[1][0] for line in res]
    return text_list

def boxes_only(result):
    '''
    
    '''
    res = result[0]
    boxes_list = [line[0] for line in res]
    return boxes_list


# test
if __name__ == "__main__":
    from PIL import Image
    from pprint import pprint

    im = Image.open("ppocr_img/imgs/11.jpg")
    pprint(ocr(from_pil(im)), indent=4)
    p = text_only(ocr(from_pil(im)))
    print(p)
