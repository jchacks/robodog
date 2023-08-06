import time

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()

# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)


def preview(timeout: int = 10):
    picam2.preview_configuration.main.size = (800, 600)
    picam2.preview_configuration.enable_lores()
    picam2.preview_configuration.lores.size = (320, 240)
    picam2.configure("preview")

    # Use Preview.QTGL for local and Preiveiw.DRM for non XWindows envs
    picam2.start_preview(Preview.QT)
    picam2.start()
    time.sleep(timeout)


def udp_stream(ip: str, port: int, timeout: int = 100):
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    encoder = H264Encoder(repeat=True, iperiod=15)
    encoder.output = FfmpegOutput(f"-f mpegts udp://{ip}:{port}")

    picam2.start_encoder(encoder)
    picam2.start()
    time.sleep(timeout)


if __name__ == "__main__":
    udp_stream()
