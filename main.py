import io

from fastapi import FastAPI
from fastapi import File
from six import string_types
from starlette.requests import Request
from starlette.responses import StreamingResponse
from tensorflow._api.v2 import image
from style_tranfer import apply_style
import ImageEfects as efect
import numpy as np
import PIL.Image as Image
import cv2 as cv
import base64
import uvicorn

app = FastAPI()

if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=9090)

@app.post('/style')
async def style(content_image: bytes = File(...),
                style_image: bytes = File(...)):

    stylized_image = apply_style(
        io.BytesIO(content_image),
        io.BytesIO(style_image),
    )

    return StreamingResponse(
        stylized_image,
        media_type="image/jpg",
    )

@app.post('/efects')
async def efects(efeito: str,
    content_image: bytes = File(...)):

    nparr= np.fromstring(content_image, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    #img_dimensions = str(img.shape)

    return_img = efect.CartoonHDR(img)

    _, encoded_img = cv.imencode('.JPG', return_img)
    encoded_img = base64.b64encode(encoded_img)

    #cimg = cv.imdecode(np.frombuffer(content_image, np.uint8), 1)
    #cimg = efect.CartoonHDR(cimg)

    # cimg = Image.fromarray(cimg)
    # teste = cv.imwrite('teste.jpg', cimg)
    # cimg = open(teste, 'rb')
    # cimg = cimg.read()

    # imagem = base64.b64encode(cimg)

    #cimg = base64.b64encode(encoded_img)
    #cimg = io.BytesIO(encoded_img)

    """
    imgOpened = Image.open(img, mode='r')
    roi_img = imgOpened.crop(Image._Box)
    roi_img.save(img, format='PNG')
    """
    
    return encoded_img
    """
    StreamingResponse(
        encoded_img,
        media_type="image/jpg"
    )
    """

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '9090'))
    except ValueError:
        PORT = 80
    app.run(HOST, PORT)

    