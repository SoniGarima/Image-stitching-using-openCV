"""Utilities
"""
import re
import base64

import numpy as np

from PIL import Image
from io import BytesIO


def base64_to_pil(img_base64):
    """
    Convert base64 image data to PIL image
    """
    print(img_base64)
    print(type(img_base64))
    img_base641=img_base64['avatar']
    img_base642=img_base64['avatar2']
    img_base641=str(img_base641)
    img_base642=str(img_base642)
    image_data = re.sub('^data:image/.+;base64,', '', img_base641)
    image_data2 = re.sub('^data:image/.+;base64,', '', img_base642)
    
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    pil_image2 = Image.open(BytesIO(base64.b64decode(image_data2)))
    return (pil_image,pil_image2)


def np_to_base64(img_np):
    """
    Convert numpy image (RGB) to base64 string
    """
    img = Image.fromarray(img_np.astype('uint8'), 'RGB')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return u"data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")

