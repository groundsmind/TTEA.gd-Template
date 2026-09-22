import cv2
import settings


class Camera:
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        self.ret, self.frame = self.stream.read()
        self.raw_frame = self.frame

        if not self.stream.isOpened():
            print("não foi possível abrir a câmera. certifique que nenhum outro processo está usando ela.")

        if self.ret and self.frame is not None:
            altura_webcam, largura_webcam, _ = self.frame.shape
            settings.largura_webcam = largura_webcam
            settings.altura_webcam = altura_webcam
            print(f"Webcam resolution: {largura_webcam}x{altura_webcam}")

    def load_camera(self):
        self.ret, self.frame = self.stream.read()
        if not self.ret or self.frame is None:
            print("Câmera indisponível")
            self.frame = None
            self.raw_frame = None
            return

        self.raw_frame = self.frame.copy()

        cv2.line(
            self.frame,
            (settings.pontos_calibracao[0]),
            (settings.pontos_calibracao[1]),
            (settings.verde),
            2,
        )
        cv2.line(
            self.frame,
            (settings.pontos_calibracao[1]),
            (settings.pontos_calibracao[3]),
            (settings.verde),
            2,
        )
        cv2.line(
            self.frame,
            (settings.pontos_calibracao[2]),
            (settings.pontos_calibracao[0]),
            (settings.verde),
            2,
        )
        cv2.line(
            self.frame,
            (settings.pontos_calibracao[2]),
            (settings.pontos_calibracao[3]),
            (settings.verde),
            2,
        )

        cv2.circle(self.frame, (settings.pontos_calibracao[0]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[1]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[2]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[3]), 5, settings.azul, 3)

    def update_camera(self):
        self.ret, self.frame = self.stream.read()

    def display_camera(self):
        if self.frame is None or self.frame.size == 0:
            print("no frames?")
            return
        cv2.imshow("Tela de Captura", self.frame)
        cv2.waitKey(1)

    def close_camera(self):
        self.stream.release()
        cv2.destroyWindow("Tela de Captura")