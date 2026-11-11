"""Stop Windows from going to sleep while a long job runs.

A laptop that sleeps in the middle of a GPU run loses its CUDA connection ("CUDA error: unknown error").
This asks Windows to stay awake only for the lifetime of the calling process; nothing in the power
settings is changed, and the request disappears when the program ends. On other systems it does nothing.
"""
from __future__ import annotations

import sys

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def keep_awake() -> None:
    if sys.platform != "win32":
        return
    import ctypes
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
