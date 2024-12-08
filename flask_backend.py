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



@app.route("/ocr/full", methods=['POST'])
def ocr_full():
    data = request.get_json()
    print("data:\n")
    print(data)
    base64_data = data['image']
    lang = data['lang']
    # Remove the base64 prefix if it exists (for example, 'data:image/png;base64,')
    if base64_data.startswith('data:image'):
        base64_data = base64_data.split(',')[1]
    im = Image.open(BytesIO(base64.b64decode(base64_data)))
    im_width=im.size[0]
    im_height=im.size[1]
    results = ocr(from_pil(im), lang = lang)
    result = results[0]
    # result is a list of [[p1,p2,p3,p4],(text, prob)]
    # p1,p2,p3,p4 are the coordinates of the box
    # with the form of [x,y]
    l =  []
    if result is None:
        print("No text detected")
        return {
            "l": []
        }
    for box, (text, prob) in result:
        x,y,w,h = box_to_rect_ratio(box,im_width, im_height)
        l.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "text": text
        })

    print(l)

    # response json
    # return result
    return {
        "l": l
    }
        

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)



