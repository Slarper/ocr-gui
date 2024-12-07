# save this as app.py
import base64
from io import BytesIO
from flask import Flask, request, send_from_directory
from PIL import ImageGrab, Image
from ocr_lib import *
from im_lib import *

app = Flask(__name__)

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')

@app.route("/ocr/clipboard")
def ocr_clipboard():
    im = ImageGrab.grabclipboard()
    result = ocr(from_pil(im))

    lines = text_only(result)
    text = "\n".join(lines)
    boxes = boxes_only(result)
    im_box = draw_polygons(im, boxes)
    im_box = resize_to_fit(im_box, 720, 720 / 1.33)
    # response json
    # json has 2 elements: text and image
    # text is utf-8 encoded string
    # image is base64 encoded image
    return {
        "text": text,
        "image": im_box
    }




# get image from json, then ocr it
@app.route("/ocr", methods=['POST'])
def ocr_req():
    # get image from json
    # image is base64 encoded
    # decode it to PIL image
    # then ocr it
    data = request.get_json()
    print(data["image"][:100])
    base64_data = data['image']
    # Remove the base64 prefix if it exists (for example, 'data:image/png;base64,')
    if base64_data.startswith('data:image'):
        base64_data = base64_data.split(',')[1]
    im = Image.open(BytesIO(base64.b64decode(base64_data)))
    result = ocr(from_pil(im))
    print(result)
    lines = text_only(result)
    text = "\n".join(lines)
    boxes = boxes_only(result)
    im_box = draw_polygons(im, boxes)
    im_box = resize_to_fit(im_box, 720, 720 / 1.33)
    # save text and image into temp/ for debugging
    im_box.save("temp/ocr_result.png")



    return {
        "text": text,
        "image": pil_image_to_base64_url(im_box)
    }


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
