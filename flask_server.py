from flask import Flask, render_template

app = Flask(__name__)

# Initial image state
current_image = "general_ocr_002.png"


@app.route("/")
def index():
    return render_template("index.html", image=current_image)


@app.route("/change_image", methods=["POST"])
def change_image():
    global current_image
    # Simple logic to switch between two images
    if current_image == "general_ocr_002.png":
        current_image = "general_ocr_002.png.svg"
    else:
        current_image = "general_ocr_002.png"
    return current_image


if __name__ == "__main__":
    app.run(debug=True)
