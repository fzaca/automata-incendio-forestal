# Automata incendio forestal

_Automata celular aplicado a incendio forestales._

_Este programa utiliza la [Vecindad de Moore](https://es.wikipedia.org/wiki/Vecindad_de_Moore), Este autómata trata de forma muy simplificada la evolución de un bosque en el que se producen incendios, podemos observar en verde a los arboles, en rojo los puntos de fuego y en gris las cenizas.
Si un arbol tiene un punto de fuego en alguna de sus 8  celdas vecinas Tiene una probabilidad (30% por defecto) de prenderse fuego, los puntos encendidos a su vez se convierten en ceniza._

<p align="center"><img src='https://raw.githubusercontent.com/Xukay101/automata-piedrapapeltijera/main/gif00.gif' /></p>

## Instrucciones 🔧

### Pre-requisitos 📋

_Es recomendable instalar un entorno virtual para las librerias aunque no es obligatorio, para ello..._

```
$ pip install virtualenv
$ python3 -m venv env
```

_Luego activa el entorno:_
```
$ source env/bin/activate
```

_Para instalar las librerias ejecuta:_

```
$ pip install -r requirements.txt
```

### Ejecucion 🚀

_Entra a la carpeta **rockpapperscissor** y ejecuta el archivo main_

```
$ python3 main.py
```

## Construido con 🛠️

* [PyGame](https://www.pygame.org/docs/) 
* [PyGame-Gui](https://pygame-gui.readthedocs.io/en/v_060/) 

## Autor ✒️

* **Jose Zacarías Flores**  - [Xukay101](https://github.com/Xukay101)
