# Desafio Crawler

Este repositório contém uma solução para o [desafio-captura](https://bitbucket.org/sievetech/desafio-captura)

Selenium + Geckodriver + BeautifulSoup
## Instalação
Python 3.6+ recomendado

1- clone o repositório

2.1 *(opcional)* - crie um [ambiente virtual](https://docs.python.org/3/library/venv.html)

2-
 ```
pip  install -r requiriments.txt
```

3- Baixe o driver [Geckodriver (v0.21.0)](https://github.com/mozilla/geckodriver/releases) de acordo com o seu Sistema Operacional

4- Extraia o driver para a pasta do repositório

## Testes

* para realizar os testes e verificar se o Geckodriver está funcionando:

```
python crawler_test.py -v
```
## Uso
```
python crawler.py
```
* O programa irá pecorrer por todas as páginas de cada categoria principal.
