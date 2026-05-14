import os.path
import threading
import cv2 as cv
import mediapipe as mp
import time
import pystray
import PIL.Image
from config import resource_path

from presence import check_user_presence
from renderer import draw_status, draw_detections
from os_actions import locking_screen
from config import MODEL_PATH, MIN_DETECTION_CONFIDENCE, LOCK_SCREEN_THRESHOLD_MS

latest_detections = []
last_seen_time = None
current_timestamp_ms = 0
running = True
paused = False
has_locked = False


def on_clicked(icon, item):
    global running, paused
    if str(item) == "Pause":
        paused = True
    elif str(item) == "Resume":
        paused = False
    elif str(item) == "Quit":
        running = False
        tray_icon.stop()


logo_path = resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphics", "tray_icon.ico"))
pillow_image = PIL.Image.open(logo_path)
tray_icon = pystray.Icon("PresenceAI", pillow_image, menu=pystray.Menu(
    pystray.MenuItem("Pause", on_clicked),
    pystray.MenuItem("Resume", on_clicked),
    pystray.MenuItem("Quit", on_clicked)
))


def callback_result(result, output_frame, timestamp):
    global current_timestamp_ms
    extract_detections(result)
    current_timestamp_ms = timestamp


def create_detector():
    base_options = mp.tasks.BaseOptions
    face_detector = mp.tasks.vision.FaceDetector
    face_detector_options = mp.tasks.vision.FaceDetectorOptions
    vision_running_mode = mp.tasks.vision.RunningMode
    options = face_detector_options(
        base_options=base_options(model_asset_path=MODEL_PATH),
        running_mode=vision_running_mode.LIVE_STREAM,
        result_callback=callback_result)
    return face_detector.create_from_options(options)


def extract_detections(detections):
    global latest_detections
    detection_data = []
    for det in detections.detections:
        origin_x, origin_y = det.bounding_box.origin_x, det.bounding_box.origin_y
        width, height = det.bounding_box.width, det.bounding_box.height
        score = det.categories[0].score

        if score > MIN_DETECTION_CONFIDENCE:
            detection_data.append({
                "x0": origin_x,
                "y0": origin_y,
                "x1": origin_x + width,
                "y1": origin_y + height,
                "score": score
            })

    latest_detections = detection_data


cap = cv.VideoCapture(0)

if not cap.isOpened():
    exit()


def detector_loop():
    global has_locked
    with create_detector() as detector:
        start_time = time.perf_counter()
        while running:
            if paused:
                time.sleep(0.2)
                continue
            ret, frame = cap.read()
            if not ret:
                break

            flipped_frame = cv.flip(frame, 1)
            image = mp.Image(data=cv.cvtColor(flipped_frame, cv.COLOR_BGR2RGB), image_format=mp.ImageFormat.SRGB)
            timestamp_ms = int((time.perf_counter() - start_time) * 1000)
            detector.detect_async(image, timestamp_ms)
            draw_detections(flipped_frame, latest_detections)
            status, absent_time_ms = check_user_presence(latest_detections, current_timestamp_ms)
            draw_status(flipped_frame, status, absent_time_ms)
            if status == "PRESENT" or status == "VERIFYING_ABSENCE":
                has_locked = False
            else:
                if absent_time_ms > LOCK_SCREEN_THRESHOLD_MS and not has_locked:
                    has_locked = True
                    locking_screen()


threading.Thread(target=detector_loop, daemon=True).start()
tray_icon.run()

cap.release()
cv.destroyAllWindows()
