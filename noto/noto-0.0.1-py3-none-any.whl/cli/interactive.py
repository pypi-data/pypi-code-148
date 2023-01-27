from noto.note.read import read
from noto.note.update import update
from noto.note.delete import delete

from noto.cli.output import print_notes
from readchar import readkey


def run(config: object):
    interactiveConfig = config.interactive
    # read note
    notes = read(
        amount=interactiveConfig.read.amount,
        min_priority=interactiveConfig.read.priority.min,
        max_priority=interactiveConfig.read.priority.max,
        random=interactiveConfig.read.random,
        tags=interactiveConfig.read.tags.only,
    )

    for note in notes:
        print_notes([note])
        print('\n')

        if not interactiveConfig.modify.skip:
            print(
                "Modifying note: Confirm (Enter), Content (c), Priority (p), Remove Tag (t), Add Tag (T), Delete Note (D), Quit (q)"
            )

            text = None
            add_tags = None
            remove_tags = None
            priority = None

            deleted = False
            while True:
                key = readkey()
                if key == "\n":
                    break
                elif key == "c":
                    text = input("New Text: ")
                elif key == "p":
                    priority = int(input("New Priority: "))
                elif key == "t":
                    tag_name = input("Tag to remove: ")
                    remove_tags = [*(remove_tags or []), tag_name]
                elif key == "T":
                    tag_name = input("Tag to add: ")
                    add_tags = [*(add_tags or []), tag_name]
                elif key == "D":
                    delete(id=note.id)
                    deleted = True
                    break
                elif key == "q":
                    return

            if not deleted:
                updated_note = update(
                    id=note.id,
                    text=text,
                    priority=priority,
                    add_tags=add_tags,
                    remove_tags=remove_tags,
                )

                print(updated_note)

    if interactiveConfig.repeat:
        run()
    else:
        return
