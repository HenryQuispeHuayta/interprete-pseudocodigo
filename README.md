# **Interprete-Pseudocodigo**

## **Ejecución**

### **Desde el código fuente**

La primera forma de ejecutar el programa es a través del código, llamando a `inFlex.py`. Para lo cual se requiere Python, que se puede descargar desde [aquí](https://www.python.org/downloads/).

Una vez instalado, se puede ejecutar de la siguiente forma:

```
python inFlex.py 
```

También se puede ejecutar un archivo específico con el siguiente comando:

```
python inFlex.py ruta-archivo/ejemplo.inf
```

Estos archivos deben tener la extensión `.inf`.

### **Instalación en el sistema**

Se puede encontrar el instalador desde los [releases](https://github.com/HenryQuispeHuayta/interprete-pseudocodigo/releases).

Una vez instalado, puede ejecutar de la siguiente forma:

```
inFlex ruta/al/archivo/ejemplo.inf
```

También, si se presenta algún problema, puede descomprimir el build y ejecutar de la siguiente forma:

```
ruta/inflex.exe ruta/al/archivo/ejemplo.inf
```

Estos archivos deben tener la extensión `.inf`.

## **Sintaxis**

### **Declaración de variables**

Para declarar una variable, se utiliza la palabra clave `var` seguida del nombre de la variable, un signo igual `=` y el valor de la variable.

Ejemplo:

```
var num = 24
var hola = "mundo"
```

### **Imprimir en pantalla**

Para imprimir en pantalla, se utiliza la función `imprimir(variable)`.

Ejemplo:

```
imprimir(1)
imprimir("hola")
```

### **Comentarios**

Para comentar código, se utiliza el símbolo `#`.

Ejemplo:

```
# Este codigo esta comentado
```

### **Estructura condicional**

La estructura condicional en pseudocódigo se define utilizando las siguientes palabras clave:

|Inglés|Español|
|-|-|
|if|si|
|then|entonces|
|elif|osi|
|else|sino|
|end|fin|

La estructura base es la siguiente:

```
si `condicion` entonces
  (hacer por si)
fin
```

```
si `condicion` entonces
  (hacer por si)
sino
  (hacer por sino)
fin
```

```
si `condicion` entonces
  (hacer por si)
osi `condicion` entonces
  (hacer por osi)
sino
  (hacer por sino)
fin
```

Ejemplo

```
var menor = 3
var mayor = 4
si menor > mayor entonces
  imprimir(menor)
osi menor < mayor entonces
  imprimir(mayor)
sino
  imprimir(0)
fin
```

### **Estructura secuencial**

La estructura secuencial se define utilizando las siguientes palabras clave:

|Inglés|Español|
|-|-|
|for|para|
|then|entonces|
|to|hasta|
|step|de|
|end|fin|

La estructura base es la siguiente:

```
para `valor inicial` hasta `valor final` entonces
  (realizar mientras se ejecute el para)
fin
```

```
para `valor inicial` hasta `valor final` de `valor incremental` entonces
  (realizar mientras se ejecute el para)
fin
```

Ejemplo:

```
para i = 1 hasta 10 entonces
  imprimir(i)
fin
```

### **Estructura repetitiva**

La estructura repetitiva se define utilizando las siguientes palabras clave:

|Inglés|Español|
|-|-|
|while|mientras|
|then|entonces|
|end|fin|

La estructura base es la siguiente:

```
mientras `condicion` entonces
  (realizar hasta salir del bucle)
fin
```

Ejemplo:

```
var i = 1
var sum = 0
mientras i < 10 entonces
  var sum = sum + i
  imprimir(sum)
  var i = i + 1
fin
```

### **Funciones**

Para definir una función se utiliza la palabra clave `funcion` seguida del nombre de la función. El bloque de la función termina con la palabra clave fin.

Ejemplo:

```
funcion saludar()
  imprimir("Hola, mundo!")
fin
```

```
funcion sumar(a, b)
  var resultado = a + b
  retornar resultado
fin
```

### **break, continue y return**

Las palabras clave `return`, `continue` y `break` se utilizan de la siguiente forma:

|Inglés|Español|
|-|-|
|return|retornar|
|continue|continuar|
|break|romper|


Su funcionamiento va de la siguiente forma:

```
para i = 1 hasta 10 entonces
  si i == 5 entonces
    romper
  fin
  imprimir(i)
fin
```

```
para i = 1 hasta 10 entonces
  si i % 2 == 0 entonces
    continuar
  fin
  imprimir(i)
fin
```

```
funcion ejemplo() entonces
  retornar 42
fin
```

## **Licencia**

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)