from PIL import Image, ImageOps
import pdfplumber
import re
import io
import fitz


def load_file(file, extension):

    if extension in ['png', 'jpg', 'jpeg']:
        im = Image.open(file)

        images = [ImageOps.exif_transpose(im)]
        order = False
    else:
        if isinstance(file, io.BytesIO):
            file = file.read()

        dpi = 250  # choose desired dpi here
        zoom = dpi / 72  # zoom factor, standard: 72 dpi
        magnify = fitz.Matrix(zoom, zoom)
        images = [page.get_pixmap(matrix=magnify).pil_image() for page in fitz.open(stream=file)]
        order = check_order(file)
    return images, order

def save_local(file):
    with open('tmp.pdf', 'wb') as f:
        f.write(file)

def check_order(pdf_file):
    pt1 = r"Согласие на обработку"
    pt2 = r"Заявление сформировано"

    save_local(pdf_file)
    with pdfplumber.open("tmp.pdf") as f:
        text = f.pages[0].extract_text()

    s1 = re.search(pt1, text) is not None
    s2 = re.search(pt2, text) is not None

    return s1 or s2

def merge(files):
    for_merge = []
    for file, ext in files:
        images, order = load_file(file, ext)
        if order:
            images.extend(for_merge)
            for_merge = images
        else:
            for_merge.extend(images)

    buf = io.BytesIO()
    for_merge[0].save(buf, save_all=True, append_images=for_merge[1::], format="pdf")

    return buf
