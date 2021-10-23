import io
from fastapi import FastAPI
from fastapi import File
from six import string_types
from starlette.requests import Request
from starlette.responses import RedirectResponse, StreamingResponse
from tensorflow._api.v2 import image
from style_tranfer import apply_style
import ImageEfects as efect
import numpy as np
import PIL.Image as Image
import cv2 as cv
import base64
import uvicorn

app = FastAPI()

# Redireciona para a página principal de schemas do Fast API (Swagger)
@app.get('/')
async def redirecting():
    return RedirectResponse(url="/docs/")

@app.post('/style')
async def style(content_image: bytes = File(...),
                style_image: bytes = File(...)):

    """Recebe dois arquivos de imagem e retorna uma imagem com características difundidas."""

    stylized_image = apply_style(
        io.BytesIO(content_image),
        io.BytesIO(style_image),
    )

    return StreamingResponse(
        stylized_image,
        media_type="image/jpg",
    )

@app.post('/efects')
async def efects(
    efeito: str,
    intensidade: int,
    content_image: bytes = File(...)):

    """ Recebe uma imagem, numeração do efeito e intensidade para aplicá-lo e retorna a imagem tratada. """

    #Converte os bytes recebidos para um array de bytes.
    nparr= np.fromstring(content_image, np.uint8)

    # Decodifica o array de bytes para uma imagem.
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    #img_dimensions = str(img.shape)

    return_img = efect.SelectAndApplyEffect(efeito, img, intensidade)
    _, encoded_img = cv.imencode('.JPG', return_img)

    #encoded_img = base64.b64encode(encoded_img)

    cimg = io.BytesIO(encoded_img)

    """
    imgOpened = Image.open(img, mode='r')
    roi_img = imgOpened.crop(Image._Box)
    roi_img.save(img, format='PNG')
    """
    return StreamingResponse(
        cimg,
        media_type="image/jpg"
    )
    #encoded_img

if __name__ == '__main__':

    """ Define o endereço e a porta de execução da aplicação """

    import os
    import uvicorn

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '80'))
    except ValueError:
        PORT = 80
    uvicorn.run(app, host = HOST, port = PORT)