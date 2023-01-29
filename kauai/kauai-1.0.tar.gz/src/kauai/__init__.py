APPS = ["kauai-finance"]


def main() -> None:
    intro: str = "Kauai is a namespace for a collection of Django apps:\n"
    print("\n   ".join([intro] + APPS))
