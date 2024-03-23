# Object Detection and Capture Application

This Python script is designed for motion detection and capture of detected objects using OpenCV library. It provides a graphical user interface (GUI) built with Tkinter for easy interaction and monitoring.

For other languages:
- Para obtener la documentación en español, consulte [Readme Español](Readme_Spanish.md).
- Para a documentação em português, consulte [Readme Portuguese](Readme_Portuguese.md).

## Features
- **Motion Detection**: Utilizes background subtraction and contour detection techniques to detect motion in the video stream.
- **Object Capture**: Captures frames containing detected objects and saves them to a specified directory.
- **Real-time Video Feed**: Displays the live video feed from connected cameras on the GUI.
- **Recording**: Initiates recording when motion is detected, saving the video with timestamps.
- **User Interface**: Offers buttons for starting and stopping detection, viewing captured images, and accessing contact information.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- Tkinter
- PIL (`Image`, `ImageTk`)
- `winsound` (Windows only)

## Usage
1. Ensure all dependencies are installed.
2. Run the script.
3. Click on "Buscar Más Cámaras" to search for available cameras.
4. Once cameras are detected, click on "Iniciar Deteccion" to start motion detection.
5. Detected objects will be highlighted, and frames containing them will be saved.
6. Click on "Detener Deteccion" to stop motion detection.
7. Use "View Captures" to open the directory containing the captured images.
8. For further assistance or inquiries, click on "Contacto" to visit the provided link.

## Contact
For support or inquiries, please visit our [Discord server](https://discord.gg/6kfbMJXKRy).
