import io
import tensorflow as tf
from PIL import Image

""" Reponsável por receber duas imagens, uma imagem alvo para aplicação de estilo de imagem
    com o conteúdo da segunda imagem de estilo, os modelos serão difundidos trazendo padrões referentes  a
    primeira imagem inserida com aspectos da segunda imagem fornecida. """

style_predict = 'tf_models/magenta_arbitrary-image-stylization-v1-256_int8_prediction_1.tflite'
style_transform = 'tf_models/magenta_arbitrary-image-stylization-v1-256_int8_transfer_1.tflite'

def img_bytes_to_array(img_bytes: io.BytesIO) -> tf.Tensor:

    """Carrega uma bytes de imagem para imagem tf tensor .
    Reescalando as cores RGB [0..255] para [0..1] e adicionar a dimensão unidimencional de bash."""

    img = tf.keras.preprocessing.image.img_to_array(
        Image.open(img_bytes)
    )
    img = img / 255  # converte [0..255] para float32 entre [0..1]
    img = img[tf.newaxis, :]  # adiciona dimensão de bash unidimensionais
    return img


def array_to_img_bytes(img_array: tf.Tensor) -> io.BytesIO:

    """Carrega uma imagem tf tensor para bytes de imagem.
    Reescalando as cores [0..1] para RGB [0..255] e adicionar a dimensão unidimencional de bash."""

    if len(img_array.shape) > 3:  # remove a dimensão de bash unidimensionais
        img_array = tf.squeeze(img_array, axis=0)
    img_array = img_array * 255  # converte [0..1] para [0..255]
    img = tf.keras.preprocessing.image.array_to_img(img_array)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='jpeg')
    img_buffer.seek(0)
    return img_buffer

def preprocess(img_tensor: tf.Tensor, target_dim: int) -> tf.Tensor:

    """Realiza um pré-processamento redimencionando um recorte central da imagem."""

    # Redimenciona a imagem para que a dimensão menor se torne a variável inserida target_dim.
    shape = tf.cast(tf.shape(img_tensor)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = target_dim / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img_tensor, new_shape)

    # Recorte central da imagem para que ambas as dimensões se tornem target_dim.
    img = tf.image.resize_with_crop_or_pad(img, target_dim, target_dim)
    return img

def run_style_predict(style_img):

    """Executa a previsão de estilo na imagem de estilo pré-processada."""

    # Carrega o modelo.
    interpreter = tf.lite.Interpreter(model_path=style_predict)

    # Definir entrada do modelo.
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], style_img)

    # Calcule as sobras de detalhes de estilo.
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    style_bottleneck = interpreter.tensor(output_details[0]["index"])()
    return style_bottleneck

def run_style_transform(style_bottleneck, content_img):

    """Executa a transformação de estilo na imagem de estilo pré-processada."""

    # Carrega o modelo.
    interpreter = tf.lite.Interpreter(model_path=style_transform)

    # Defini entrada do modelo.
    input_details = interpreter.get_input_details()
    interpreter.allocate_tensors()

    # Defini as entradas dos modelos.
    interpreter.set_tensor(input_details[0]["index"], content_img)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()

    # Transforma a imagem do conteúdo.
    output_details = interpreter.get_output_details()
    stylized_image = interpreter.tensor(output_details[0]["index"])()
    return stylized_image

def apply_style(content_image: io.BytesIO,
                style_image: io.BytesIO) -> io.BytesIO:

    """Aciona todos os métodos anteriores para realizar o tratamento das imagens e retorna a imagem final resultante."""

    content_img = preprocess(img_bytes_to_array(content_image), 384)
    style_img = preprocess(img_bytes_to_array(style_image), 256)

    style_bottleneck = run_style_predict(style_img)
    stylized_image = run_style_transform(style_bottleneck, content_img)

    stylized_image = array_to_img_bytes(stylized_image)
    return stylized_image
