import io
import os
import re

from PIL import Image
from urllib.parse import urlparse
from common.log import logger

def fsize(file):
    if isinstance(file, io.BytesIO):
        return file.getbuffer().nbytes
    elif isinstance(file, str):
        return os.path.getsize(file)
    elif hasattr(file, "seek") and hasattr(file, "tell"):
        pos = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(pos)
        return size
    else:
        raise TypeError("Unsupported type")


def compress_imgfile(file, max_size):
    if fsize(file) <= max_size:
        return file
    file.seek(0)
    img = Image.open(file)
    rgb_image = img.convert("RGB")
    quality = 95
    while True:
        out_buf = io.BytesIO()
        rgb_image.save(out_buf, "JPEG", quality=quality)
        if fsize(out_buf) <= max_size:
            return out_buf
        quality -= 5


def split_string_by_utf8_length(string, max_length, max_split=0):
    encoded = string.encode("utf-8")
    start, end = 0, 0
    result = []
    while end < len(encoded):
        if max_split > 0 and len(result) >= max_split:
            result.append(encoded[start:].decode("utf-8"))
            break
        end = min(start + max_length, len(encoded))
        # 如果当前字节不是 UTF-8 编码的开始字节，则向前查找直到找到开始字节为止
        while end < len(encoded) and (encoded[end] & 0b11000000) == 0b10000000:
            end -= 1
        result.append(encoded[start:end].decode("utf-8"))
        start = end
    return result



def get_path_suffix(path):
    path = urlparse(path).path
    return os.path.splitext(path)[-1].lstrip('.')


def convert_webp_to_png(webp_image):
    from PIL import Image
    try:
        webp_image.seek(0)
        img = Image.open(webp_image).convert("RGBA")
        png_image = io.BytesIO()
        img.save(png_image, format="PNG")
        png_image.seek(0)
        return png_image
    except Exception as e:
        logger.error(f"Failed to convert WEBP to PNG: {e}")
        raise


def remove_markdown_symbol(text: str):
    # 移除markdown格式，目前先移除**
    if not text:
        return text
    return re.sub(r'\*\*(.*?)\*\*', r'\1', text)