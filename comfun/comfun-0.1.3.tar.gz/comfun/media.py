import logging
import re
import pyperclip


def grab_tstamps(fpath: str, copy_to_clipboard=True):
    """
    Grabs timestamps from a txt file with time stamps in (HH:)MM:SS format (one per line), and returns them in
    mp3splt's minutes.seconds[.hundredths] format.
    :param fpath:
    :return:
    """
    with open(fpath, "r") as f:
        lines = f.readlines()

    timestamps = []
    # Regex eeds to be on reversed tstamp in order to work so that the optional hour value comes at the END.
    pattern = re.compile(r"(?P<second>\d\d):(?P<minute>\d*):?(?P<hour>\d*)?")
    for line in lines:

        line_reversed = line.strip()[::-1]
        match = pattern.match(line_reversed)
        if match:
            hour, minute, second = match["hour"], match["minute"], match["second"]

            if hour.strip():
                hour = int(hour[::-1])
            minute = int(minute[::-1])
            second = int(second[::-1])

            logging.debug(f"H: {hour}, M: {minute}, S: {second}")
            if not hour:
                hour = 0
            hour = int(hour)
            minutes = minute + hour * 60
            timestamps.append(f"{minutes:04}.{second:02}")

    timestamps = sorted(list(set(timestamps)))  # rm duplicates
    timestamps = " ".join(timestamps)
    print(timestamps)

    if copy_to_clipboard:
        pyperclip.copy(timestamps)
    return timestamps

if __name__ == "__main__":
    fpath = "/home/findux/Desktop/tstamps"
    grab_tstamps(fpath)