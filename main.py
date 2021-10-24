from enum import Enum
import io
from fastapi import FastAPI
from fastapi import File
from fastapi.datastructures import Default, DefaultType
from six import string_types
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response, StreamingResponse
from tensorflow._api.v2 import image
from style_tranfer import apply_style
import ImageEfects as efect
import numpy as np
import PIL.Image as Image
import cv2 as cv
import base64
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

description = """
API do projeto de atividades práticas supervisionadas (APS) de processamento de imagens.

Integrantes do grupo: 

    N3855J3 - WESLEY MARCOS M DOS SANTOS
    F0359E1 - LUCAS CAMPANUCHI CORREA
    N429160 - WELLINGTON F DE OLIVEIRA
    N485HJ6 - VINICIUS ALVES PANOBIANCO

Conteúdo didático para apresentação de projeto.

"""

app = FastAPI(
    title="API - Editor de imagens online",
    description=description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE" , "GET" , "POST" , "PUT" ],
    allow_headers=["*"],
)


# Redireciona para a página principal de schemas do Fast API (Swagger)
@app.get('/', include_in_schema=False)
def redirecting():
    return RedirectResponse(url="/docs",status_code=302)

@app.post('/estilo')
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

class Efeitos(str, Enum):
    ef1 = "Desfoque"
    ef2 = "Blur"
    ef3 = "Blur_bilateral"
    ef5 = "Escala_cinza"
    ef6 = "Ajuste_brilho"
    ef7 = "Pintura"
    ef8 = "Foto_sepia"
    ef9 = "HDR"
    ef10 = "Inverter_Cores"
    ef11 = "Cores_Quentes"
    ef12 = "Cores_frias"
    ef13 = "Desenho_lapis"
    ef14 = "Desenho_lapis_cores"
    ef15 = "Filtro_cartoon"
    ef16 = "Cartoon_HDR"

@app.post('/efeitos')
async def efects(
    efeito: Efeitos,
    intensidade: int ,
    content_image: bytes = File(...)):

    """ Recebe uma imagem, numeração do efeito e intensidade para aplicá-lo e retorna a imagem tratada. """

    #Converte os bytes recebidos para um array de bytes.
    nparr= np.fromstring(content_image, np.uint8)

    # Decodifica o array de bytes para uma imagem.
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    #img_dimensions = str(img.shape)

    # Aplica o efeito escolhido na imagem e retorna bytes_array da imagem
    try:
        return_img = efect.SelectAndApplyEffect(efeito, img, intensidade)
        _, encoded_img = cv.imencode('.JPG', return_img)
        #cimg = io.BytesIO(encoded_img)
        encoded_img = base64.b64encode(encoded_img)
        return encoded_img
        """ return StreamingResponse(
        cimg,
        media_type="image/jpg"
        ) """
    except:
        return JSONResponse(
            status_code=400,
            content={"message": f"Oops! Código de filtro ou parâmetro de intensidade incorreto!"}
        )

    #encoded_img = base64.b64encode(encoded_img)
    
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