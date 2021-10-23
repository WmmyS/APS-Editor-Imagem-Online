import cv2 as cv
import numpy as np
from scipy.interpolate import UnivariateSpline

path = "../image/imagem.jpg"
img = cv.imread(path)

# Recebe como parâmetros o arquivo de imagem e nível de intensidade
def imageSmoothing(img, intesity):
    blur = cv.blur(img,(intesity,intesity))
    return blur

# Recebe uma imagem e aplica um filtro de blur
def imageFiltering(img):
    kernel = np.ones((5,5),np.float32)/25
    dst = cv.filter2D(img,-1,kernel)
    return dst

# Recebe uma imagem e retorna a imagem com o bluor bilateral
def bilateralFiltering(img):
    blur = cv.bilateralFilter(img,9,75,75)
    return blur

# Reduz o ruido de imagem com zoom ou com cores fragmentadas
def denoising(img):
    image = cv.imread(img)
    dst = cv.fastNlMeansDenoisingColored (image, None , 10,10,7,21)
    return dst

# Retorna uma imagem com escala de tons de cinza
def greyscale(img):
    grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return grayscale

# Ajuste de brilho de imagem
def brigth(img, percentual):
    img_bright = cv.convertScaleAbs(img, beta=percentual)
    return img_bright

# Efeito de pintura
def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    img_sharpen = cv.filter2D(img, -1, kernel)
    return img_sharpen

# Efeito de foto sépia
def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) 
    img_sepia = cv.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) 
    img_sepia[np.where(img_sepia > 255)] = 255 
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia

#Efeito HDR
def HDR(img):
    hdr = cv.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return  hdr

# Efeito de inversão de cores
def InvertColors(img):
    return cv.bitwise_not(img)

# Salva um arquivo de uma determinada extensão
def result(img, name, extension):
    return cv.imwrite("{}.{}".format(name, extension), img)

# Função de pesquisa em tabela de escalas para aplicação de filtro
def LookupTable(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))

# Efeito de verão
def SummerEffect(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel  = cv.split(img)
    red_channel = cv.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    sum= cv.merge((blue_channel, green_channel, red_channel ))
    return sum

# Efeito de inverno
def WinterEffect(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv.split(img)
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win= cv.merge((blue_channel, green_channel, red_channel))
    return win

# Efeito de desenho à lápis
def PencilSketchEffectGray(img):
    # Aplica efeito de lápis na imagem em tons de cinza
    sk_gray, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_gray

# Efeito de desenho à lápis com cores dominantes da imagem
def PencilSketchEffectColorful(img):
    sk_gray, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_color

#Efeito de cartoon na imagem
def CartoonEffect(img):
    edges1 = cv.bitwise_not(cv.Canny(img, 100, 200))
    dst = cv.edgePreservingFilter(img, flags=2, sigma_s=64, sigma_r=0.25)
    cartoon1 = cv.bitwise_and(dst, dst, mask=edges1)
    return cartoon1

#Efeito de cartoon na imagem e HDR
def CartoonHDR(img):
    return HDR(CartoonEffect(img))

#plot(img, sharpen(img))
# cv.imwrite('../image/resultado/teste.jpg', InvertColors(img))