import string
import emoji
from tif.fabric import cli

class Logger:
    def __init__(self) -> None:
        pass

    def log(self, message : string):
        """
        Outputs white message to console with :bell: emoji
        """
        cli.puts("** {} {}".format(emoji.emojize(':bell:'), message))

    def info(self, message : string):
        """
        Outputs white message to console with :memo: emoji
        """
        cli.puts("*** {} {}".format(emoji.emojize(':memo:'), message))
    
    def error(self, message : string):
        """
        Outputs red message to console with :red_exclamation_mark: emoji
        """
        cli.puts("error: {} {}".format(emoji.emojize(':red_exclamation_mark:'), message))

    def success(self, message : string):
        """
        Outputs green message to console
        """
        cli.puts(".:~ {}".format(message))
    
    def log_custom(self, color_key : string, message : string, emoji_string : None):
        """
        Outputs a custom message to console. Allows to specify a color and emoji for the message
        """
        if emoji:
            cli.puts("{} {} {}".format(color_key, emoji.emojize(emoji_string), message))
        else:
            cli.puts("{} {}".format(color_key, message))