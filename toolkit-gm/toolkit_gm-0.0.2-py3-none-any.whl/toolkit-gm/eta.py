import datetime
from misc import percent

class Eta:
    """Object to follow execution advancement."""

    def __init__(self) -> None:
        self.begin_time = 0
        self.length = 0
        self.current_count = 0
        self.last_display_time = 0
        self.text = ''


    def begin(self, length, text) -> None:
        """Start a counter."""

        self.length = length
        self.current_count = 0
        self.text = text

        now = datetime.datetime.now().timestamp()
        self.begin_time = now

        print(self.text + ' - Elapsed: [00h00\'00] - ETA [??h??\'??] - ' + percent(0))
        self.last_display_time = now


    def iter(self, force_print=False) -> None:
        """On an iteration."""

        self.current_count += 1
        now = datetime.datetime.now().timestamp()

        timeSinceLastDisplay = now - self.last_display_time

        if (now - timeSinceLastDisplay < 1) and not force_print: return

        time_spent = now - self.begin_time
        percent_spent = self.current_count / self.length

        if(percent_spent != 0): time_left = (time_spent / percent_spent) - time_spent
        else: time_left = 0

        # Calculations
        hours_elapsed = int(time_spent / 3600)
        minutes_elapsed = int((time_spent - (3600 * hours_elapsed)) / 60)
        seconds_elapsed = int(round(time_spent - (60 * minutes_elapsed + 3600 * hours_elapsed)))
        hours_left =  int(time_left / 3600)
        minutes_left = int((time_left - (3600 * hours_left)) / 60)
        seconds_left = int(round(time_left - (60 * minutes_left + 3600 * hours_left)))

        # Stringify to right format
        hours_elapsed = '{:0>2.0f}'.format(hours_elapsed)
        minutes_elapsed = '{:0>2.0f}'.format(minutes_elapsed)
        seconds_elapsed = '{:0>2.0f}'.format(seconds_elapsed)
        hours_left = '{:0>2.0f}'.format(hours_left)
        minutes_left = '{:0>2.0f}'.format(minutes_left)
        seconds_left = '{:0>2.0f}'.format(seconds_left)

        print('\033[1A\033[K' + self.text + f' - Elapsed: [{hours_elapsed}h{minutes_elapsed}\'{seconds_elapsed}] - ETA [{hours_left}h{minutes_left}\'{seconds_left}] - ' + percent(percent_spent))
        self.last_display_time = now


    def end(self) -> None:
        """Finalize an ETA counting."""

        now = datetime.datetime.now().timestamp()

        # Calculations
        total_time = now - self.begin_time
        total_hours = int(total_time / 3600)
        total_minutes = int((total_time - (3600 * total_hours)) / 60)
        total_sec = int(total_time - (60 * total_minutes + 3600 * total_hours))

        # Stringify to right format
        total_hours = '{:0>2.0f}'.format(total_hours)
        total_minutes = '{:0>2.0f}'.format(total_minutes)
        total_sec = '{:0>2.0f}'.format(total_sec)

        print('\033[1A\033[K' + self.text + f' is done - Elapsed: [{total_hours}h{total_minutes}\'{total_sec}]')


    def log(self, string) -> None:
        """Print out a log, without messing with the ETA display."""

        print(string)
        self.iter(force_print=True)

