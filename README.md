 An OCR GUI powered by PaddleOCR.

 It reads the image from clipboard, so another screenshot tool such as Snipaste is required.


# Install Dependecies

inside or outside a virtual environment:
```
pip install -r requirements.txt
```

# Run

```
python tk.py
```

# Pack to exe(Build)

There are 2 approaches:

1. pyinstaller command:

```
pyinstaller --noconfirm --onefile --windowed --hidden-import "imghdr" --hidden-import "imgaug" --hidden-import "pyclipper" --collect-data "paddle" --collect-all "paddleocr"  "C:\Users\naive\ocr-gui\tk.py"
```

2. auto-py-to-exe config json:

    1. install auto-py-to-exe: `pip install auto-py-to-exe`

    2. run `auto-py-to-exe`

    3. choose the `apte.json` in Settings > Import Config From Json File

# Web Update

Since AI models are large, maybe a better way to hold the application is in the form of web application.

I have made a web-equivalent of tk.py. check it by

```sh
python flask_backend.py
```
