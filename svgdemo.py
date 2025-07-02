import svgwrite
import base64


def create_svg_with_embedded_image(output_file, image_path):
    # Create SVG drawing
    dwg = svgwrite.Drawing(output_file, size=("800px", "600px"))

    # Add background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#f0f0f0"))

    # Embed image as base64
    def embed_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/{image_path.split('.')[-1]};base64,{encoded}"

    # Add embedded image
    dwg.add(dwg.image(href=embed_image(image_path), insert=(50, 50), size=(200, 200)))

    # Add multiple styled text elements
    texts = [
        {
            "content": "Main Title",
            "pos": (300, 100),
            "size": 40,
            "weight": "bold",
            "color": "navy",
        },
        {
            "content": "Subtitle Text",
            "pos": (300, 150),
            "size": 24,
            "color": "darkgreen",
        },
        {
            "content": "Body text with details",
            "pos": (300, 200),
            "size": 16,
            "color": "black",
        },
        {
            "content": "Additional information",
            "pos": (300, 250),
            "size": 14,
            "color": "#666",
            "font": "Arial, sans-serif",
        },
    ]

    for text in texts:
        dwg.add(
            dwg.text(
                text["content"],
                insert=text["pos"],
                font_size=f"{text['size']}px",
                font_weight=text.get("weight", "normal"),
                fill=text["color"],
                font_family=text.get("font", "inherit"),
            )
        )

    # Save SVG
    dwg.save()
    print(f"SVG created with embedded image at {output_file}")


# Usage - replace 'your_image.jpg' with your image file
create_svg_with_embedded_image("embedded_output.svg", "your_image.jpg")
