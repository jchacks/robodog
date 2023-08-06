import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

# Use Preview.QTGL for local and Preiveiw.DRM for non XWindows envs
picam2.start_preview(Preview.QT)
picam2.start()
time.sleep(10)
picam2.capture_file("/tmp/test.jpg")
