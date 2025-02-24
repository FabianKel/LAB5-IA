# LABORATORIO 5 - Inteligencia Artificial
# Proyecto: Resolución de Laberintos con Búsqueda en Anchura

[Enlace al repositorio](https://github.com/FabianKel/LAB5-IA)

## Integrantes del equipo
- [Mónica Salvatierra - 22249](https://github.com/alee2602)
- [Paula Barillas - 22764](https://github.com/paulabaal12)
- [Derek Arreaga - 22537](https://github.com/FabianKel) 

## Descripción

Este laboratorio implementa un algoritmo de búsqueda en anchura (BFS) para resolver laberintos representados como imágenes. El programa convierte la imagen en una representación discreta, resuelve el laberinto y visualiza la solución.

## Requisitos

Antes de ejecutar el programa, asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install opencv-python numpy
```

## Ejecución
Para ejecutar el programa, utiliza el siguiente comando en la terminal:
```bash
python main.py
```
Luego, se solicitará ingresar la ruta de la imagen del laberinto (Ej: Test2.bmp).
El programa leerá la imagen, la discretizará, resolverá el laberinto utilizando BFS y mostrará la solución gráficamente.

## Funcionamiento
1. Se carga la imagen del laberinto y se discretiza en una matriz de celdas.

    | Input | Output |
    |----------|----------|
    | ![alt text](readme_files/image.png)    |![alt text](readme_files/image-1.png)  |

2. Se define el problema del laberinto con un estado inicial y un estado objetivo.
3. Se ejecuta la búsqueda en anchura (BFS) para encontrar el camino desde el inicio hasta la meta.
4. Se reconstruye el camino de la solución y se muestra paso a paso.
    ```bash
        Solución encontrada:
        Paso 1: (34, 35) - Inicio
        Paso 2: (33, 35) - Moverse arriba
        Paso 3: (32, 35) - Moverse arriba
        Paso 4: (31, 35) - Moverse arriba
        Paso 5: (30, 35) - Moverse arriba
        Paso 6: (29, 35) - Moverse arriba
        Paso 7: (28, 35) - Moverse arriba
        Paso 8: (27, 35) - Moverse arriba
        Paso 9: (26, 35) - Moverse arriba
        Paso 10: (26, 34) - Moverse izquierda
        Paso 11: (26, 33) - Moverse izquierda
        Paso 12: (26, 32) - Moverse izquierda
        Paso 12: (26, 32) - Moverse izquierda
        Paso 13: (25, 32) - Moverse arriba
        Paso 14: (24, 32) - Moverse arriba
        Paso 12: (26, 32) - Moverse izquierda
        ..., etc.
    ```
    

5. Se visualiza el laberinto con la solución marcada en color.
<center>

![alt text](readme_files/image-2.png)

</center>