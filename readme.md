# Aplicación de Detección movimiento

Este módulo contiene la implementación de una aplicación de detección de movimiento que utiliza OpenCV y Tkinter.

## Descripción

La aplicación captura un video en tiempo real desde una cámara web y detecta objetos en movimiento en el video utilizando sustracción de fondo y detección de contornos. Además, la aplicación permite guardar capturas de los nuevos objetos detectados en una carpeta específica.

## Funcionalidades

- **Inicio y detención de la detección de objetos:** La aplicación permite iniciar y detener la detección de objetos en el video en vivo.
- **Interfaz gráfica de usuario (GUI) interactiva:** Utiliza Tkinter para crear una interfaz gráfica fácil de usar que muestra el video en tiempo real y proporciona botones para controlar la detección de objetos.
- **Detección de objetos en movimiento:** Utiliza el algoritmo de sustracción de fondo y la detección de contornos para identificar objetos en movimiento en el video.
- **Guardado de capturas de objetos detectados:** Las capturas de los nuevos objetos detectados se guardan en una carpeta especificada para su posterior revisión.

## Instalación

Antes de ejecutar la aplicación, asegúrate de tener las siguientes dependencias instaladas:

- **OpenCV:** Para el procesamiento de imágenes y la detección de objetos.
- **Tkinter:** Para la creación de la interfaz gráfica de usuario.
- **winsound:** (Solo en Windows) Para la reproducción de sonidos al detectar movimiento.

Puedes instalar las dependencias utilizando pip:

```bash
pip install opencv-python
```

## Uso

Para ejecutar la aplicación, simplemente ejecuta el archivo `Main.py`. Esto iniciará la aplicación y abrirá una ventana que muestra el video en tiempo real de tu cámara web.

- Haz clic en el botón "Start Detection" para activar la detección de objetos en movimiento.
- Haz clic en el botón "Stop Detection" para detener la detección de objetos.
- Haz clic en el botón "View Captures" para abrir la carpeta que contiene las capturas de los nuevos objetos detectados.
