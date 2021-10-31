# **APS Processamento de Imagem BACK-END**

<p align="justify">O objetivo desse projeto é criar uma aplicação de processamento de imagem com uma interface web e uma API no back-end em python aplicando filtros nas imagens e retornando para o front-end.

## **Configurando API back-end para uso**

<p align="justify">*Neste exemplo mostrarei como testar a API no Windows em um abiente de desenvolvimento dentro do vscode, más caso queira, pode também instalar as bibliotecas em seu sistema para testar.*

## Requisitos:

Ter instalado em seu ambiente o Python 3 na versão 3.7+ para funcionamento de todas a bibliotecas;

Ter instalado o pip Python na versão 21.3.1 para instalação dos recursos.

### Preparando o ambiente:

No terminal digite o seguinte comando seguinte para preparar um ambiente venv:

``` python3 -m venv env ```

Para entrar no ambiente digite:

``` env/Scripts/activate ```

Dentro do ambiente instale as dependências:

Fast API

``` pip install "fastapi[all]" ```

Open CV

``` pip install opencv-python ```

Spicy

``` pip install -U scipy ```

Pillow

``` pip install -U pillow ```

Tensorflow

``` pip install tensorflow ```

A porta padrão da API está em localhost:80, definido no trecho abaixo dentro do arquivo main.py :

