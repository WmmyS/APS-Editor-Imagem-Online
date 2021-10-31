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
  
Verá que está dentro do ambiente de desenvolvimento no terminal que antes do diret´rorio ficará com a sigla (env) da seguinte forma:
  
  ![image](https://user-images.githubusercontent.com/53191767/139586334-83123ca7-5ed3-439b-b907-71f7f818283f.png)


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
  
  ![image](https://user-images.githubusercontent.com/53191767/139586248-bbb6effa-2bb2-4a6a-8c8d-f94cb54369ec.png)

No vscode para executar a aplicação você poderá precionar F5 ou executar no Start debugging:
  
 ![image](https://user-images.githubusercontent.com/53191767/139586606-7237b700-218b-47b7-88fe-7f97bd2660c1.png)

No terminal irá apresentar a seguinte mensagem:
  
  ![image](https://user-images.githubusercontent.com/53191767/139586686-4effde42-c822-4e09-ac02-05ead8a640fd.png)

Acessanto a url http://localhost:80 será direcionado para a url de documentação do Swagger:
  
  ![image](https://user-images.githubusercontent.com/53191767/139586861-828ac6e7-7fdc-4518-8cac-ffdf93da7a73.png)


