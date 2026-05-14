import os
import cv2 as cv
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


BASE_DIR = resource_path(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = resource_path(os.path.join(
    BASE_DIR,
    "models",
    "blaze_face_full_range.tflite"
))

LOCK_SCREEN_THRESHOLD_MS = 20000
VERIFYING_ABSENCE_THRESHOLD_MS = 2000

MIN_DETECTION_CONFIDENCE = 0.6

BOX_COLOR = (0, 0, 150)
BOX_THICKNESS = 2

FONT = 0
FONT_SCALE = 0.7
TEXT_COLOR = (0, 0, 150)
TEXT_THICKNESS = 1
TEXT_FONT = cv.FONT_HERSHEY_SIMPLEX
