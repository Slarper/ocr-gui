from paddleocr import PaddleOCR


import sys


def process_file(input_path, output_path):
    """
    Reads content from input file and writes it to output file.

    Args:
        input_path (str): Path to the input file
        output_path (str): Path to the output file
    """
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,  # Disables document orientation classification model via this parameter
        use_doc_unwarping=False,  # Disables text image rectification model via this parameter
        use_textline_orientation=False,  # Disables text line orientation classification model via this parameter
    )
    # ocr = PaddleOCR(lang="en") # Uses English model by specifying language parameter
    # ocr = PaddleOCR(ocr_version="PP-OCRv4") # Uses other PP-OCR versions via version parameter
    # ocr = PaddleOCR(device="gpu") # Enables GPU acceleration for model inference via device parameter
    # ocr = PaddleOCR(
    #     text_detection_model_name="PP-OCRv5_mobile_det",
    #     text_recognition_model_name="PP-OCRv5_mobile_rec",
    #     use_doc_orientation_classify=False,
    #     use_doc_unwarping=False,
    #     use_textline_orientation=False,
    # ) # Switch to PP-OCRv5_mobile models
    result = ocr.predict(input_path)
    for res in result:
        res.print()
        # res.save_to_img(output_path)
        res.save_to_json(output_path)


if __name__ == "__main__":
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python file_processor.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_file(input_file, output_file)
