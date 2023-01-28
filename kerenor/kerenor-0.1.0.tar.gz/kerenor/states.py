import os
from dataclasses import dataclass


IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

THOUGHT = os.path.join(IMGS_PATH, "thought.png")
WHAT = os.path.join(IMGS_PATH, "what.png")
ZEN = os.path.join(IMGS_PATH, "zen.png")
NO = os.path.join(IMGS_PATH, "no.png")


@dataclass
class Screen:
    text: str
    bg_path: str
    font: str = "Helvetica 16"

    def __hash__(self):
        return hash(self.text)


@dataclass
class Option:
    text: str
    next: Screen


start = Screen(text="Oi, what do you want?", bg_path=WHAT)
idea = Screen(text="Well, what do you have in mind?", bg_path=THOUGHT)
idea_r = Screen(text="NO.\nThat's a terrible idea.\nThink about it some\n more.", bg_path=NO, font="Helvetica 18 bold")
can_we = Screen(text="Hmmm so what do we need to do?", bg_path=THOUGHT)
kai = Screen(text="Are you Kai?", bg_path=WHAT)
kai_y = Screen(text="NO. We can't do that.", bg_path=NO, font="Helvetica 18 bold")
kai_n = Screen(text="Well, everything is a trade off.\nConsider first what is required functionally - meaning, "
                    "what does the thing NEED to do at all, then consider performance requirements.\nQuestions to ask yourself-\n"
                    " - Where are the bottlenecks?\n"
                    " - What is a reasonable load? What increases it? (more cameras? users? msgs?)\n"
                    " - Where can load be distributed & handling parallelized? (more services of some type? servers?)\n"
                    " - Where can requirements be relaxed? (example, in History-saving requirement of latency is relaxed)\n"
                    "Remember that no system can do all the load with all the accuracy and zero latency.\n"
                    "The important part of being a SW engineer is finding which trade-offs are relevant to your case right now.\n"
                    "I'm afraid ChatGPT won't help in many cases, BUT most problems are already \"solved problems\" - "
                    "someone already had to deal with them - so it's always wise to see what other people did in similar cases and learn.\n"
                    "Best of luck!", bg_path=ZEN, font="Helvetica 13")
back_option = Option(text="Ask something else", next=start)

BYE_TXT = "Nevermind, bye!"

StateM = {
    start: [Option(text="Say, how can we do the thing?", next=can_we),
            Option(text="I have an idea I wanna discuss", next=idea)],
    idea: [Option(text="Tell me about your idea\nclick here when done", next=idea_r)],
    idea_r: [back_option],
    can_we: [Option(text="Tell me what we need to do\nclick here when done", next=kai)],
    kai: [Option(text="yes", next=kai_y), Option(text="no", next=kai_n)],
    kai_y: [back_option],
    kai_n: [back_option]
}
