import base64
from io import BytesIO
from PIL import ImageDraw, Image


def draw_polygon(im, vertices):
    """
    im : PIL.Image

    vertices : is in the form of [[x1,y1],[x2,y2],...]

    """

    # Create a Draw object
    draw = ImageDraw.Draw(im)

    # # Define the four vertices of the quadrilateral (四边形)
    # vertices = [(100, 100), (300, 100), (350, 300), (50, 300)]
    vertices = [tuple(vertex) for vertex in vertices]

    # Define the color (red)
    polygon_color = (255, 0, 0)

    # Draw the quadrilateral
    draw.polygon(vertices, outline=polygon_color, width=4)

    return im

def draw_polygons(im, vertices_list):
    """
    im : PIL.Image

    vertices : is in the form of [[x1,y1],[x2,y2],...], so 
    
    vertices_list : is in the form of [vertices1, vertices2,...]

    """
    # Create a Draw object
    draw = ImageDraw.Draw(im)

    # # Define the four vertices of the quadrilateral (四边形)
    # vertices = [(100, 100), (300, 100), (350, 300), (50, 300)]

    # Define the color (red)
    polygon_color = (255, 0, 0)

    for vertices in vertices_list:
        vertices = [tuple(vertex) for vertex in vertices]
    # Draw the quadrilateral
        draw.polygon(vertices, outline=polygon_color, width=2)

    return im

def resize_to_fit(image, target_width, target_height):
    '''
    image : PIL.Image
    target_width : int
    target_height : int

    Resizes an image to fit within a given width and
    height. None of them can be exceded.
    '''
    # Get the original width and height of the image
    original_width, original_height = image.size

    # Calculate the aspect ratios for both dimensions
    width_ratio = target_width / original_width
    height_ratio = target_height / original_height

    # Use the smaller ratio to ensure the image fits within the target dimensions
    scaling_factor = min(width_ratio, height_ratio)

    # Calculate the new dimensions
    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    return resized_image

def pil_image_to_base64_url(image: Image, image_format: str = 'PNG') -> str:
    """
    Convert a PIL Image object to a base64-encoded data URI string.
    
    :param image: PIL Image object.
    :param image_format: The format to save the image (default is PNG).
    :return: A base64-encoded data URI string for the image.
    """
    # Create a BytesIO buffer to hold the image data
    buffered = BytesIO()

    # Save the image to the buffer in the specified format (e.g., PNG or JPEG)
    image.save(buffered, format=image_format)

    # Get the base64-encoded bytes
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Construct the data URI (for example, for PNG images)
    data_uri = f"data:image/{image_format.lower()};base64,{base64_image}"

    return data_uri
