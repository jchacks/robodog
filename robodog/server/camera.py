import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.DRM)
picam2.start()
time.sleep(10)
picam2.capture_file("/tmp/test.jpg")
