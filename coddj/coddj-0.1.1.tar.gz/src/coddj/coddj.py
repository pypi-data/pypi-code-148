from __future__ import print_function, unicode_literals

from PyInquirer import prompt
import random
from search import search
from player import play_song
from pyfiglet import Figlet


EXIT_TOGGLE = False
queue = []

def main():
    
    questions = [
        {
            "type": "list",
            "name": "mode",
            "message": "Mode: ",
            "choices": ["search", "playlist"],
        }
    ]
    mode = prompt(questions).get("mode")
    if mode == "search":
      query = query_mode()
    elif mode == "playlist":
      get_file_name()
      query = shuffle_playlist()
    search_results = search(query)

    choice = list_search_results(search_results)

    play_song(choice['search'])

    return prompt_to_continue()


def get_file_name():
  questions = [
    {
      "type": "input",
      "name": "filename",
      "message": "Playlist File: ",
    }
  ]
  filename = prompt(questions).get("filename")
  with open(filename, 'r') as f:
    data = f.read()
  data = data.split("\n")
  for line in data:
    queue.append(line)
  #return filename.get("filename")
  
  
def shuffle_playlist():
  if len(queue) > 0:
    choice = random.choice(queue)
    queue.remove(choice)
    return choice
  else:
    return ""


def query_mode():
  questions = [
    {
      "type": "input",
      "name": "query",
      "message": "Search: ",
    }  
  ]
  query = prompt(questions)
  return query.get("query")


def list_search_results(search_list):
    questions = [
        {
            "type": "list",
            "name": "search",
            "message": "Search Results: ",
            "choices": search_list,
        }
    ]
    answer = prompt(questions)
    return answer


def prompt_to_continue():
    questions = [
        {
            "type": "confirm",
            "message": "Do you want to continue?",
            "name": "continue",
            "default": True
        }
    ]

    answer = prompt(questions)
    return not answer['continue']


if __name__ == "__main__":
    f = Figlet(font="slant")
    print(f.renderText("MP3 Player"))

    while True:
        try:
            if EXIT_TOGGLE:
                break
            EXIT_TOGGLE = main()
        except KeyboardInterrupt:
            break
        print("Exiting, goodbye!")
