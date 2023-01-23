from colorama import Fore


def colourise(value, colour, condition=None):
    """Colour a piece of text. If a condition callback is passed in, the text will only be
    coloured if the condition is met.
    """
    if condition is not None:
        if not condition(value):
            return str(value)
    return f"{colour}{value}{Fore.RESET}"


def success(text):
    return colourise(text, Fore.GREEN)


def success_negative(text):
    return colourise(text, Fore.LIGHTRED_EX)


def progress(text):
    return colourise(text, Fore.CYAN)


def warning(text):
    return colourise(text, Fore.RED)


def confirm(message=""):
    prompt_message = colourise("\nDo you want to continue? [y/N] ", Fore.LIGHTBLUE_EX)
    response = input(f"{message}{prompt_message}")
    return response.lower() in ("y", "yes")


def confirm_dangerous_command():
    message = (
        "You are about to execute a dangerous command against a"
        f" {colourise('production' , Fore.RED)} environment. Please ensure you are pairing with"
        " someone else."
    )
    # TODO. Include an actual multi person MFA to proceed.
    if not confirm(message):
        print(success_negative("Aborted."))
        raise SystemExit
