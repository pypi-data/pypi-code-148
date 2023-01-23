#!/usr/bin/env python3
import json
import re
import string
import sys
from urllib import parse
import urllib.request as request
from .prompts import user_choice, InvalidCmdPrompt, InputError
from .system import open_process


def add_files(user, add: list):
    """
    Add the given list of args to the users playlist file.
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    urls = []
    for file in add:
        if is_url(file) or is_magnet(file):
            urls.append(file)
        else:
            playlist[file] = file
    if urls is not None:
        for url in urls:
            title = process_url(url)
            playlist[title] = url
    with open(user.files["playlist_file"], "w") as data:
        json.dump(playlist, data, indent=4)
    return 0


def ask_user(options, user, prompt):
    """
    Ask a user something and handle any errors, return False if the user
    reponds with nothing or error is caught
    """
    try:
        choice = user_choice(options=options, user=user, prompt=prompt)
    except (InvalidCmdPrompt, InputError, KeyboardInterrupt) as err:
        print(err, sys.stderr)
        return False
    if choice is None:
        return False
    return choice


def delete_item(user, item):
    """
    Delete the given item from user's playlist.
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    if item not in playlist:
        print(f"WARNING: {item} is not in your playlist", file=sys.stderr)
        return 1
    playlist.pop(item, None)
    with open(user.files["playlist_file"], "w") as data:
        json.dump(playlist, data, indent=4)
    return 0


def display_playlist(user, ask=True):
    """
    Display users playlist
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    if ask:
        choice = ask_user(options=playlist.keys(), user=user, prompt="Play: ")
        if not choice:
            return 1
        chosen = playlist[choice]
        playlist.pop(choice, None)
        cmd = mpv_cmd(item=[chosen], items=playlist.values())
    else:
        cmd = mpv_cmd(item=playlist.values())
    open_process(opener=cmd)
    return 0


def is_magnet(filename):
    """
    Detect if a filename is a magnet link
    """
    return re.match("magnet:", filename)


def is_url(filename):
    """
    This is the same method mpv uses to decide this
    """
    parts = filename.split("://", 1)
    if len(parts) < 2:
        return False
    # protocol prefix has no special characters => it's an URL
    allowed_symbols = string.ascii_letters + string.digits + "_"
    prefix = parts[0]
    return all(map(lambda c: c in allowed_symbols, prefix))


def mpv_cmd(item, items=None):
    """
    Return a command list to feed to system.open_process
    if a path to the item is given it the two will be joined
    """
    mpv_list = [
        "mpv",
        "--script-opts=dmenuplaylist-enabled=yes",
        "--loop-playlist=no",
        "--keep-open=no",
    ]
    if items is not None:
        item.extend(items)
    mpv_list.extend(item)
    return mpv_list


def process_url(url):
    """
    Process urls
    """
    # use some regex and urllib.parse.unquote to get titles for magnet links
    # figure out some way to get titles for youtube videos
    # change structure to dict with title as the key and actual url/file as the value
    if is_magnet(url):
        raw_title = parse.unquote(url)
        prog = re.compile(r"&dn=(.*)&xl=")
    else:
        page = request.urlopen(url)
        raw_title = page.read().decode("utf8")
        prog = re.compile(r"<meta property=\"og:title\" content=\"(.*)\">\n")
    title_match = prog.search(raw_title)
    if title_match is not None:
        return title_match.group(1)
    return url


def remove_item(user):
    """
    Remove selected items from user's playlist
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    choice_flag = True
    while choice_flag:
        choice = ask_user(options=playlist, user=user, prompt="Play: ")
        if not choice:
            choice_flag = False
            continue
        playlist.pop(choice, None)
    with open(user.files["playlist_file"], "w") as data:
        json.dump(playlist, data, indent=4)
    return 0
