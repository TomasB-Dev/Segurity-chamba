# Aplicación de Detección y Captura de Objetos

Este script en Python está diseñado para la detección de movimiento y captura de objetos detectados utilizando la biblioteca OpenCV. Proporciona una interfaz gráfica de usuario (GUI) construida con Tkinter para una interacción y monitoreo fáciles.

## Características
- **Detección de Movimiento**: Utiliza técnicas de sustracción de fondo y detección de contornos para detectar movimiento en el flujo de video.
- **Captura de Objetos**: Captura fotogramas que contienen objetos detectados y los guarda en un directorio especificado.
- **Transmisión de Video en Tiempo Real**: Muestra la transmisión de video en vivo de las cámaras conectadas en la GUI.
- **Grabación**: Inicia la grabación cuando se detecta movimiento, guardando el video con marcas de tiempo.
- **Interfaz de Usuario**: Ofrece botones para iniciar y detener la detección, ver imágenes capturadas y acceder a la información de contacto.

## Requisitos
- Python 3.x
- OpenCV (`cv2`)
- Tkinter
- PIL (`Image`, `ImageTk`)
- `winsound` (solo en Windows)

## Uso
1. Asegúrese de que todas las dependencias estén instaladas.
2. Ejecute el script.
3. Haga clic en "Buscar Más Cámaras" para buscar cámaras disponibles.
4. Una vez detectadas las cámaras, haga clic en "Iniciar Deteccion" para comenzar la detección de movimiento.
5. Los objetos detectados se resaltarán, y se guardarán los fotogramas que los contienen.
6. Haga clic en "Detener Deteccion" para detener la detección de movimiento.
7. Use "Ver Capturas" para abrir el directorio que contiene las imágenes capturadas.
8. Para obtener más ayuda o consultas, haga clic en "Contacto" para visitar el enlace proporcionado.

## Contacto
Para soporte o consultas, por favor visite nuestro [servidor de Discord](https://discord.gg/6kfbMJXKRy).
