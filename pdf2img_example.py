from pdf2image import convert_from_path

images = convert_from_path("linear-type-can-change-the-world.pdf",dpi=300)

for i, image in enumerate(images):
    image.save(f"pdf2-imgs/page_{i + 1}.jpg", "JPEG")
