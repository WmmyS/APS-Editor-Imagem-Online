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
from pydantic import BaseModel

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
    ef1 = "Filtro cartoon"
    ef2 = "Blur"
    ef3 = "Blur bilateral"
    ef5 = "Escala cinza"
    ef6 = "Cartoon HDR"
    ef7 = "Pintura"
    ef8 = "Foto sepia"
    ef9 = "HDR"
    ef10 = "Inverter Cores"
    ef11 = "Cores Quentes"
    ef12 = "Cores frias"
    ef13 = "Lapis"
    ef14 = "Lapis Cores"

@app.get('/listarefeitos')
def print():
    try:
        return list(Efeitos)
    except:
        return JSONResponse(
            status_code=400,
            content={"message": f"Oops! Código de filtro ou parâmetro de intensidade incorreto!"}
        )

# Objeto para receber a string do código base64 no corpo da requisição
class Item(BaseModel):
    code: str

@app.post('/efeitos')
async def efects(
    efeito: Efeitos,
    intensidade: int ,
    content_image: Item ):

    """ Recebe uma imagem, numeração do efeito e intensidade para aplicá-lo e retorna a imagem tratada. """

    try:
        # Decodifica de uma string de código base64 para um buffer de imagem
        content_image = base64.b64decode(content_image.code)

        # Converte de buffer para um byte-array de imagem
        content_image = np.frombuffer(content_image, np.uint8)

        # Decodifica o array em imagem
        content_image = cv.imdecode(content_image, cv.IMREAD_COLOR)
    except:
        return JSONResponse(
            status_code=400,
            content={"message" : f"Erro! Código de imagem base64 corrompido!"}
        )

    return_img = efect.SelectAndApplyEffect(efeito, content_image, intensidade)
    _, encoded_img = cv.imencode('.JPG', return_img)
    encoded_img = base64.b64encode(encoded_img)
    return encoded_img

    # Aplica o efeito escolhido na imagem e retorna bytes_array da imagem
    """ try:
        return_img = efect.SelectAndApplyEffect(efeito, content_image, intensidade)
        _, encoded_img = cv.imencode('.JPG', return_img)
        encoded_img = base64.b64encode(encoded_img)
        return encoded_img
    except:
        return JSONResponse(
            status_code=400,
            content={"message": f"Oops! Código de filtro ou parâmetro de intensidade incorreto!"}
        ) """

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