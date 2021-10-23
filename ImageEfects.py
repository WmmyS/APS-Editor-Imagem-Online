import cv2 as cv
import numpy as np
from scipy.interpolate import UnivariateSpline

path = "../image/imagem.jpg"
img = cv.imread(path)

"""Responsável pelos efeitos a serem aplicados nas imagens fornecidas, os métodos com os respectivos
   efeitos deverão sem chamados pela aplicação para retorna a imagem tratada com o efeito selecionado."""

# Efeito 1
# Recebe como parâmetros o arquivo de imagem e nível de intensidade.
def imageSmoothing(img, intensity):
    blur = cv.blur(img,(intensity,intensity))
    return blur

# Efeito 2
# Recebe uma imagem e aplica um filtro de blur.
def imageFiltering(img):
    kernel = np.ones((5,5),np.float32)/25
    dst = cv.filter2D(img,-1,kernel)
    return dst

# Efeito 3
# Recebe uma imagem e retorna a imagem com o bluor bilateral.
def bilateralFiltering(img):
    blur = cv.bilateralFilter(img,9,75,75)
    return blur

# Efeito 4
# Reduz o ruido de imagem com zoom ou com cores fragmentadas.
def denoising(img):
    image = cv.imread(img)
    dst = cv.fastNlMeansDenoisingColored (image, None , 10,10,7,21)
    return dst

# Efeito 5
# Retorna uma imagem com escala de tons de cinza.
def greyscale(img):
    grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return grayscale

# Efeito 6
# # Ajuste de brilho de imagem com um percentual fornecido.
def brigth(img, percentual):
    img_bright = cv.convertScaleAbs(img, beta=percentual)
    return img_bright

# Efeito 7
# Efeito de pintura.
def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    img_sharpen = cv.filter2D(img, -1, kernel)
    return img_sharpen

# Efeito 8
# Efeito de foto sépia.
def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) 
    img_sepia = cv.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) 
    img_sepia[np.where(img_sepia > 255)] = 255 
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia

# Efeito 9
#Efeito HDR.
def HDR(img):
    hdr = cv.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return  hdr

# Efeito 10
# Efeito de inversão de cores.
def InvertColors(img):
    return cv.bitwise_not(img)

def result(img, name, extension):
    """ Salva um arquivo de uma determinada extensão."""
    return cv.imwrite("{}.{}".format(name, extension), img)

def LookupTable(x, y):
    """Função de pesquisa em tabela de escalas para aplicação de filtro."""
    spline = UnivariateSpline(x, y)
    return spline(range(256))

# Efeito 11
# Efeito de verão.
def SummerEffect(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel  = cv.split(img)
    red_channel = cv.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    sum= cv.merge((blue_channel, green_channel, red_channel ))
    return sum

# Efeito 12
# Efeito de inverno.
def WinterEffect(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv.split(img)
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win= cv.merge((blue_channel, green_channel, red_channel))
    return win

# Efeito 13
# Efeito de desenho à lápis.
def PencilSketchGrayEffect(img):
    # Aplica efeito de lápis na imagem em tons de cinza.
    sk_gray, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_gray

# Efeito 14
# Efeito de desenho à lápis com cores dominantes da imagem.
def PencilSketchColorfulEffect(img):
    sk_gray, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_color

# Efeito 15
# Efeito de cartoon na imagem.
def CartoonEffect(img):

    # Finding the Edges of Image
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    gray = cv.medianBlur(gray, 7) 
    edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 10)
    # Making a Cartoon of the image
    color = cv.bilateralFilter(img, 12, 250, 250) 
    cartoon = cv.bitwise_and(color, color, mask=edges)

    """ edges1 = cv.bitwise_not(cv.Canny(cartoon, 100, 200))
    dst = cv.edgePreservingFilter(cartoon, flags=2, sigma_s=64, sigma_r=0.25)
    cartoon1 = cv.bitwise_and(dst, dst, mask=edges1) """
    return cartoon

# Efeito 16
# Efeito de cartoon na imagem e HDR.
def CartoonHDR(img):
    return HDR(CartoonEffect(img))

def SelectAndApplyEffect(number, img, intensity):

    """Recebe um némero referente ao efeito a ser executado, uma imagem a ser tratada
       e um parâmentro para ser inserido no método quando houver."""

    if   number == "1":
        if intensity == "" :
            intensity = "1"
        return imageSmoothing(img, intensity)
    elif number == "2":
        return imageFiltering(img)
    elif number == "3":
        return bilateralFiltering(img)
    elif number == "4":
        return denoising(img)
    elif number == "5":
        return greyscale(img)
    elif number == "6":
        if intensity == "" :
            intensity = "1"
        return brigth(img, intensity)
    elif number == "7":
        return sharpen(img)
    elif number == "8":
        return sepia(img)
    elif number == "9":
        return HDR(img)
    elif number == "10":
        return InvertColors(img)
    elif number == "11":
        return SummerEffect(img)
    elif number == "12":
        return WinterEffect(img)
    elif number == "13":
        return PencilSketchGrayEffect(img)
    elif number == "14":
        return PencilSketchColorfulEffect(img)
    elif number == "15":
        return CartoonEffect(img)
    elif number == "16":
        return CartoonHDR(img)
    elif number == "":
        return "Efeito não encontrado"

#plot(img, sharpen(img))
# cv.imwrite('../image/resultado/teste.jpg', InvertColors(img))