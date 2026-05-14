last_seen_time = None


def check_user_presence(presence, timestamp_ms: int):
    global last_seen_time
    status, absent_time = "", 0
    if presence:
        last_seen_time = timestamp_ms
        status, absent_time = "PRESENT", 0
    else:
        if last_seen_time is not None:
            absent_time = timestamp_ms - last_seen_time
            if absent_time < 2000:
                status = "VERIFYING_ABSENCE"
            else:
                status = "ABSENT"
    return status, absent_time
