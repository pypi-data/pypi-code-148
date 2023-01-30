got_setproctitle = False

try:
    import setproctitle

    got_setproctitle = True
except Exception:
    pass


def modify_process_title(title):
    global got_setproctitle

    if got_setproctitle:
        old_title = setproctitle.getproctitle()
        if not old_title.startswith("["):
            new_title = f"[{title}] {old_title}"
            setproctitle.setproctitle(new_title)
