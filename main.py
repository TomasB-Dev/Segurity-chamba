"""
Este módulo contiene la implementación de una aplicación de detección de movimiento.
"""
import os
from datetime import datetime

import winsound

import cv2
import tkinter as tk
# pylint: disable=no-member
class ObjectDetectionApp:
    """Clase para la aplicación de detección de objetos."""
    def __init__(self, root):
        """Inicializa la aplicación."""
        self.root = root
        self.root.title("Segurity Chamba")
        self.root.geometry("800x600")

        self.detector_on = False
        self.output_directory = "nuevos_objetos"
        os.makedirs(self.output_directory, exist_ok=True)
        self.image_count = 0

        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.detected_objects = {}
        self.ignore_time = 10

        self.cap = cv2.VideoCapture(0)
        self.video_frame = tk.Label(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.root,bg="black")
        self.control_frame.pack(fill=tk.X)

        self.start_button = tk.Button(self.control_frame, text="Start Detection",bg="green2", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(self.control_frame, text="Stop Detection",bg="red", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_captures_button = tk.Button(self.control_frame, text="View Captures", command=self.view_captures)
        self.view_captures_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_video()

    def update_video(self):
        """
    Actualiza continuamente el marco de video mostrado en la interfaz de usuario.
    
    Captura un nuevo fotograma del video en vivo y lo muestra en el widget de la interfaz gráfica de usuario.
    Si la detección de objetos está activada, también se ejecuta el método detect_objects para buscar objetos en el fotograma.
    """
        ret, frame = self.cap.read()
        if ret:
            if self.detector_on:
                self.detect_objects(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = cv2.resize(frame, (800, 480))
            photo = cv2.cvtColor(photo, cv2.COLOR_RGB2BGR)
            photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
            photo = tk.PhotoImage(data=cv2.imencode('.png', photo)[1].tobytes())
            self.video_frame.config(image=photo)
            self.video_frame.image = photo
        self.video_frame.after(10, self.update_video)

    def start_detection(self):
        """
            Activa la detección de objetos en el video en vivo.

            Cambia el estado del detector a activado y deshabilita el botón de inicio.
        """
        self.detector_on = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_detection(self):
        """
            Detiene la detección de objetos en el video en vivo.

            Cambia el estado del detector a desactivado y habilita el botón de inicio.
        """
        self.detector_on = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def detect_objects(self, frame):
        """
    Detecta objetos en el marco dado utilizando sustracción de fondo y detección de contornos.

    Args:
        frame: El marco de entrada del flujo de video.

    Returns:
        None
        """
        fgmask = self.fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        fgmask = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]

        contours, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            now = datetime.now()

            if (x, y, w, h) in self.detected_objects:
                last_detected_time = self.detected_objects[(x, y, w, h)]
                time_difference = (now - last_detected_time).total_seconds()
                if time_difference < self.ignore_time:
                    continue

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite(os.path.join(self.output_directory, f"nuevo_objeto_{self.image_count}.jpg"), frame)
            self.image_count += 1
            self.detected_objects[(x, y, w, h)] = now
            # Reproducir sonido cuando se detecte movimiento
            winsound.PlaySound("Alarma.mp3", winsound.SND_ASYNC)

    def view_captures(self):
        """
            Abre la carpeta que contiene las capturas de los nuevos objetos detectados.

            Utiliza el método `os.startfile()` para abrir la carpeta en el explorador de archivos del sistema.
        """
        os.startfile(os.path.abspath(self.output_directory))

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()
