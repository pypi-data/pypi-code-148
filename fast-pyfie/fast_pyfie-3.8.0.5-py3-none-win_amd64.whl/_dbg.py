import os

ENABLE_DEBUG = False

# 外部環境変数からのデバッグ出力制御.
_DISABLE_DEBUG_PRINT = True if "PYFIE_DISABLE_DEBUG_PRINT" in os.environ else False


def disable_debug_print():
    _DISABLE_DEBUG_PRINT = True


def enable_debug_print():
    _DISABLE_DEBUG_PRINT = False


def DEBUG_PRINT(*args):
    if True == ENABLE_DEBUG and False == _DISABLE_DEBUG_PRINT:
        print(*args)


def DEBUG_TRACE_PRINT():
    import traceback
    if True == ENABLE_DEBUG:
        traceback.print_exc()
