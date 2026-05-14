from config import *


def draw_detections(frame, detections):
    for detection in detections:
        cv.rectangle(frame, (detection["x0"], detection["y0"]), (detection["x1"], detection["y1"]),
                     color=BOX_COLOR,
                     thickness=2)
        cv.putText(frame, f"User presence: {round(detection["score"], 2)}",
                   (detection["x0"] + 10, detection["y0"] - 10),
                   TEXT_FONT, 0.6, color=(0, 0, 150))


def draw_status(frame, status, away_time):
    if status == "PRESENT":
        cv.putText(frame, "STATUS: PRESENT", (400, 20), TEXT_FONT, FONT_SCALE, TEXT_COLOR,
                   thickness=TEXT_THICKNESS)
    elif status == "VERIFYING_ABSENCE":
        cv.putText(frame, "VERIFYING_ABSENCE", (400, 20), TEXT_FONT, FONT_SCALE, TEXT_COLOR,
                   thickness=TEXT_THICKNESS)
    elif status == "ABSENT":
        cv.putText(frame, "STATUS: ABSENT", (400, 20), TEXT_FONT, FONT_SCALE, TEXT_COLOR,
                   thickness=TEXT_THICKNESS)
        cv.putText(frame, f"AWAY: {round((away_time / 1000), 1)}", (400, 40), TEXT_FONT,
                   FONT_SCALE,
                   TEXT_COLOR, thickness=TEXT_THICKNESS)
