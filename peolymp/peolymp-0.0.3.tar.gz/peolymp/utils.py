import math
import os


def get_many(f, item_filter=None):
    items = []
    offset = 0
    size = 100
    while True:
        m = f(offset=offset, size=size)
        for item in m.items:
            if item_filter is None or item_filter(item):
                items += [item]
        if len(m.items) != size:
            break
        offset += size
        print(offset)
    return items


def download_sources_by_data(dest, contest, problems, participants, submissions):
    def lang_ext(lang):
        if ":" in lang:
            lang = lang[:lang.find(":")]
        if lang == "bf":
            return "bf"
        if lang == "csharp":
            return "cs"
        if lang == "d":
            return "d"
        if lang == "pascal":
            return "pas"
        if lang == "go":
            return "go"
        if lang in ["gpp", "cpp"]:
            return "cpp"
        if lang == "haskell":
            return "hs"
        if lang == "java":
            return "java"
        if lang == "js":
            return "js"
        if lang == "kotlin":
            return "kt"
        if lang == "lua":
            return "lua"
        if lang == "php":
            return "php"
        if lang in ["pypy", "python"]:
            return "py"
        if lang == "ruby":
            return "rb"
        if lang == "rust":
            return "rs"
        if lang == "c":
            return "c"
        if lang == "plain":
            return "txt"
        print('Language not found:', lang)
        return "txt"

    ends_at = contest.ends_at.seconds

    problems_dict = dict({})
    for problem in problems:
        problems_dict[problem.id] = chr(ord('a') + problem.index - 1)

    participants_dict = dict({})
    for participant in participants:
        participants_dict[participant.id] = participant.name

    for submission in submissions:
        if submission.submitted_at.seconds > ends_at:
            continue
        username = submission.participant_id

        if submission.participant_id in participants_dict:
            username = participants_dict[submission.participant_id]

        path = "{}/{}/{}/{}_{}.{}".format(
            dest,
            username,
            problems_dict[submission.problem_id],
            submission.submitted_at.seconds,
            math.floor(submission.percentage * 100),
            lang_ext(submission.lang)
        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as file:
            file.write(submission.source)
