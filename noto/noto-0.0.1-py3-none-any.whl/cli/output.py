from noto.model import Note


def print_notes(notes: list[Note]):
    print("\n".join([n.__repr__() for n in notes]))
