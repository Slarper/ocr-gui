from PIL import Image, ImageDraw

# Open an image
image = Image.open("somefile.png")

# Create a Draw object
draw = ImageDraw.Draw(image)

# Define the four vertices of the quadrilateral (四边形)
vertices = [(100, 100), (300, 100), (350, 300), (50, 300)]

# Define the color (red)
polygon_color = (255, 0, 0)

# Draw the quadrilateral
draw.polygon(vertices, outline=polygon_color, width=5)

# Save or display the image
image.save("image_with_quadrilateral.jpg")
image.show()
