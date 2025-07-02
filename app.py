import gradio as gr
from paddleocr import PaddleOCR
import svgwrite
import base64
from PIL import Image
import numpy as np
import io
import tempfile
import json
import os

# 初始化 OCR 模型（只加载一次）
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


def pil_to_base64(pil_image):
    """将 PIL 图像编码为 base64 字符串"""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def create_svg_with_ocr(pil_image):
    """主逻辑：OCR + 保存 JSON + 生成 SVG"""

    # 创建临时文件保存图片
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img_file:
        pil_image.save(tmp_img_file.name)
        image_path = tmp_img_file.name

    # 使用新版 PaddleOCR 接口 predict()
    result = ocr.predict(image_path)
    if not result:
        return "<p style='color:red'>识别失败或未检测到文本。</p>"

    result = result[0]  # predict 返回的是 list

    # 保存 JSON 到临时路径
    output_dir = tempfile.mkdtemp()
    result.save_to_json(output_dir)
    json_path = os.path.join(
        output_dir, os.path.basename(image_path).replace(".png", "_res.json")
    )

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    text_list = data.get("rec_texts", [])
    pos_list = data.get("rec_boxes", [])

    # 取左上角坐标作为文字位置
    pos_list = [(x[0], x[1]) for x in pos_list]

    # 构造 SVG
    width, height = pil_image.size
    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))

    # 嵌入图片
    dwg.add(
        dwg.image(href=pil_to_base64(pil_image), insert=(0, 0), size=(width, height))
    )

    # 叠加文字
    for text, pos in zip(text_list, pos_list):
        dwg.add(
            dwg.text(
                text,
                insert=pos,
                font_size="12px",
                fill="red",
                class_="copy-text",
            )
        )

    # 清理临时文件
    os.remove(image_path)
    os.remove(json_path)

    svg_str = dwg.tostring()

    # 加上 CSS + JS 脚本
    html_output = f"""
    {svg_str}
    """

    return html_output


# Gradio 页面搭建
with gr.Blocks(title="图像文字识别 SVG 工具") as demo:
    gr.Markdown(
        "## 🧠 图像 OCR + SVG 标注（新版PaddleOCR）\n上传或粘贴图像，右侧显示带可复制文字的 SVG 结果。"
    )

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(
                label="上传或粘贴图片", sources=["upload", "clipboard"], type="pil"
            )
        with gr.Column():
            svg_output = gr.HTML(label="识别结果 SVG")

    image_input.change(fn=create_svg_with_ocr, inputs=image_input, outputs=svg_output)

demo.launch()
