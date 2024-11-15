from pix2text import Pix2Text

img_fp = "tests/formu.png"
p2t = Pix2Text.from_config()
outs = p2t.recognize_formula(img_fp)
print(outs)
