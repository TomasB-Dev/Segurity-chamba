"""
    Deteccion de movimiento y captura del mismo
"""
import os
from datetime import datetime
import winsound
import tkinter as tk
import webbrowser
import cv2
from PIL import Image, ImageTk

# pylint: disable=no-member
class ObjectDetectionApp:
    """Clase para la aplicación de detección de objetos."""
    def __init__(self, root):
        """Inicializa la aplicación."""
        self.root = root
        self.root.title("Segurity Chamba")
        self.root.geometry("825x520")
        self.root.iconbitmap("icono.ico")

        self.detector_on = False
        self.output_directory = "nuevos_objetos"
        os.makedirs(self.output_directory, exist_ok=True)
        self.image_count = 0

        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.detected_objects = {}
        self.ignore_time = 10

        self.timer_running = False
        self.start_time = None
        self.record_duration = 30 # Duración de la grabación en segundos
        self.video_writer = None
        self.detector_on = False
        self.is_recording = False

        self.cameras = []

        self.top_camera_frame = tk.Frame(self.root, bg="black")
        self.top_camera_frame.pack(fill=tk.X)

        self.bottom_camera_frame = tk.Frame(self.root, bg="black")
        self.bottom_camera_frame.pack(fill=tk.X)

        self.control_frame = tk.Frame(self.root, bg="black")
        self.control_frame.pack(fill=tk.X)

        self.search_cameras_button = tk.Button(
            self.control_frame, text="Buscar Más Cámaras",
            command=self.search_cameras
        )
        self.search_cameras_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.start_button = tk.Button(
            self.control_frame, text="Iniciar Deteccion", bg="green2",
            command=self.start_detection, state=tk.DISABLED
        )
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(
            self.control_frame, text="Detener Deteccion", bg="red",
            command=self.stop_detection, state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_captures_button = tk.Button(
            self.control_frame, text="View Captures",
            command=self.view_captures
        )
        self.view_captures_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.link_button = tk.Button(
            self.control_frame, text="Contacto",
            command=self.open_link
        )
        self.link_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_video()
    def open_link(self):
        """Abrir enlace."""
        webbrowser.open("https://discord.gg/6kfbMJXKRy")

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
                    camera_frame = tk.Label(self.top_camera_frame,
                                            text="Cámara no encontrada",
                                            bg="blue", fg="white", width=60, height=15,
                                            relief=tk.SUNKEN, borderwidth=2)
                    if i < 2:
                        camera_frame = tk.Label(self.top_camera_frame,
                                                text="Cámara no encontrada",
                                                bg="blue", fg="white", width=60, height=15,
                                                relief=tk.SUNKEN, borderwidth=2)
                    else:
                        camera_frame = tk.Label(self.bottom_camera_frame,
                                        text="Cámara no encontrada", bg="blue", fg="white",
                                        width=60, height=15, relief=tk.SUNKEN, borderwidth=2)
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
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        camera_frame.config(image=photo)
        camera_frame.image = photo

    def start_detection(self):
        """Activar la detección de objetos."""
        self.detector_on = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.timer_running = False
        # Iniciar la grabación del video
        frame_width = int(self.cameras[0][0].get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cameras[0][0].get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_filename = f"video_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
        video_path = os.path.join(self.output_directory, video_filename)
        self.video_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (frame_width, frame_height))
        self.start_time = datetime.now()  # Registrar el tiempo de inicio de la grabación

    def stop_detection(self):
        """Detener la detección de objetos."""
        self.detector_on = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.timer_running = False
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
    def detect_objects(self, frame):
        """
        Detecta objetos en el marco dado utilizando
        sustracción de fondo y detección de contornos.

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
            cv2.imwrite(os.path.join(self.output_directory,
                                    f"nuevo_objeto_{self.image_count}.jpg"), frame)
            self.image_count += 1
            self.detected_objects[(x, y, w, h)] = now
            winsound.PlaySound("Alarma.wav", winsound.SND_ASYNC)

            self.start_time = datetime.now()

            # Iniciar la grabación si no se está grabando actualmente
            if not self.is_recording:
                self.is_recording = True
                frame_width = int(self.cameras[0][0].get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(self.cameras[0][0].get(cv2.CAP_PROP_FRAME_HEIGHT))
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_filename = f"video_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
                video_path = os.path.join(self.output_directory, video_filename)
                self.video_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (frame_width, frame_height))
                self.start_time = datetime.now()  # Registrar el tiempo de inicio de la grabación

            # Continuar grabando mientras la detección de objetos esté activa
            if self.is_recording:
                if self.video_writer is not None:
                    self.video_writer.write(frame)

        # Detener la grabación después de 30 segundos sin movimiento
        if self.is_recording:
            time_since_start = (datetime.now() - self.start_time).total_seconds()
            if time_since_start >= self.record_duration:
                self.is_recording = False
                if self.video_writer is not None:
                    self.video_writer.release()
                    self.video_writer = None

    def stop_video(self):
        """
            Detiene la grabación de video.
        """
        self.timer_running = False
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

    def view_captures(self):
        """
        Abre la carpeta que contiene las capturas de los nuevos objetos detectados.
        """
        os.startfile(os.path.abspath(self.output_directory))

    def update_video(self):
        """
        Actualiza continuamente el marco de video mostrado en la interfaz de usuario.
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
