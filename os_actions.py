import ctypes


def locking_screen():
    ctypes.windll.user32.LockWorkStation()
