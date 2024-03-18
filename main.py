import os
from datetime import datetime
import winsound
import tkinter as tk
import cv2

# pylint: disable=no-member
class ObjectDetectionApp:
    """Clase para la aplicación de detección de objetos."""
    def __init__(self, root):
        """Inicializa la aplicación."""
        self.root = root
        self.root.title("Segurity Chamba")
        self.root.geometry("825x520")

        self.detector_on = False
        self.output_directory = "nuevos_objetos"
        os.makedirs(self.output_directory, exist_ok=True)
        self.image_count = 0

        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.detected_objects = {}
        self.ignore_time = 10

        self.cameras = []

        # Frame para las cámaras superiores
        self.top_camera_frame = tk.Frame(self.root, bg="black")
        self.top_camera_frame.pack(fill=tk.X)

        # Frame para las cámaras inferiores
        self.bottom_camera_frame = tk.Frame(self.root, bg="black")
        self.bottom_camera_frame.pack(fill=tk.X)

        self.control_frame = tk.Frame(self.root, bg="black")
        self.control_frame.pack(fill=tk.X)

        self.search_cameras_button = tk.Button(self.control_frame, text="Buscar Más Cámaras", command=self.search_cameras)
        self.search_cameras_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.start_button = tk.Button(self.control_frame, text="Start Detection", bg="green2", command=self.start_detection, state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(self.control_frame, text="Stop Detection", bg="red", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_captures_button = tk.Button(self.control_frame, text="View Captures", command=self.view_captures)
        self.view_captures_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_video()

    def search_cameras(self):
        """Buscar y mostrar cámaras disponibles."""
        if not self.cameras:
            for i in range(4):
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                if ret:
                    camera_frame = tk.Label(self.top_camera_frame, bg="black")
                    if i < 2:
                        camera_frame = tk.Label(self.top_camera_frame, bg="black")
                    else:
                        camera_frame = tk.Label(self.bottom_camera_frame, bg="black")
                    camera_frame.pack(side=tk.LEFT, padx=5, pady=5)
                    self.cameras.append((cap, camera_frame))
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.view_captures_button.config(state=tk.NORMAL)
                else:
                    camera_frame = tk.Label(self.top_camera_frame, text="Cámara no encontrada", bg="blue", fg="white", width=60, height=15, relief=tk.SUNKEN, borderwidth=2)
                    if i < 2:
                        camera_frame = tk.Label(self.top_camera_frame, text="Cámara no encontrada", bg="blue", fg="white", width=60, height=15, relief=tk.SUNKEN, borderwidth=2)
                    else:
                        camera_frame = tk.Label(self.bottom_camera_frame, text="Cámara no encontrada", bg="blue", fg="white", width=60, height=15, relief=tk.SUNKEN, borderwidth=2)
                    camera_frame.pack(side=tk.LEFT, padx=5, pady=5)
                    self.cameras.append((None, camera_frame))
        else:
            for cap, camera_frame in self.cameras:
                if cap is None:
                    camera_frame.config(text="Cámara no encontrada", bg="blue", fg="white")
                else:
                    camera_frame.config(text="")
                    ret, frame = cap.read()
                    if ret:
                        self.show_camera(frame, camera_frame)
                    else:
                        camera_frame.config(text="Cámara no disponible", bg="blue", fg="white")

    def show_camera(self, frame, camera_frame):
        """Mostrar el fotograma de la cámara en el marco."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (423, 227))
        photo = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        photo = tk.PhotoImage(data=cv2.imencode('.png', photo)[1].tobytes())
        camera_frame.config(image=photo)
        camera_frame.image = photo

    def start_detection(self):
        """Activar la detección de objetos."""
        self.detector_on = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_detection(self):
        """Detener la detección de objetos."""
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

            #  verifica si un objeto detectado con las coordenadas `(x, y,
            # w, h)` ha sido detectado previamente dentro de un cierto período de tiempo especificado por
            # `self.ignore_time`.
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
            winsound.PlaySound("Alarma.wav", winsound.SND_ASYNC)

    def view_captures(self):
        """
            Abre la carpeta que contiene las capturas de los nuevos objetos detectados.

            Utiliza el método `os.startfile()` 
            para abrir la carpeta en el explorador de archivos del sistema.
        """
        os.startfile(os.path.abspath(self.output_directory))

    def update_video(self):
        """
            Actualiza continuamente el marco de video mostrado en la interfaz de usuario.
    
            Captura un nuevo fotograma del video en vivo y lo muestra en el widget de la interfaz gráfica de usuario.
            Si la detección de objetos está activada, también se ejecuta el método detect_objects para buscar objetos en el fotograma.
        """
        for cap, camera_frame in self.cameras:
            if cap is not None:
                ret, frame = cap.read()
                if ret:
                    if self.detector_on:
                        self.detect_objects(frame)
                    self.show_camera(frame, camera_frame)
                else:
                    camera_frame.config(text="Cámara no disponible", bg="blue", fg="white")
        self.root.after(10, self.update_video)

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()
