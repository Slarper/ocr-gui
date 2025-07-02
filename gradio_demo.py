import gradio as gr


def process_image(img):
    # 你可以在这里处理 img（如 OCR + 生成 SVG）
    # 这里用一个固定 SVG 示例替代
    svg = """
    <svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
      <rect width="200" height="100" fill="white"/>
      <text x="10" y="50" font-size="20" fill="black">这是识别结果</text>
    </svg>
    """
    return svg
with open("general_ocr_002.png.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(
                type="pil", label="上传或粘贴图片", sources=["upload", "clipboard"]
            )
        with gr.Column():
            svg_output = gr.HTML(svg_content)

    # 图片变化时调用函数，更新右侧 SVG
    image_input.change(fn=process_image, inputs=image_input, outputs=svg_output)

demo.launch()
