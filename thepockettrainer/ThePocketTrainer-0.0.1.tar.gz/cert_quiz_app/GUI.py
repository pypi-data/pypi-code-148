
from tkinter import StringVar
import tkinter as tk

import pandas as pd


class Flashcard:
    def __init__(self):
        self.questions = pd.read_csv("questions.csv")
        self.current_question_index = 0


    def get_question(self):
        self.question = self.questions.iloc[self.current_question_index]
        return self.question

    def get_num_questions(self):
        return len(self.questions)


class Quiz:
    def __init__(self):
        self.flashcard = Flashcard()
        
        self.num_correct = 0

    def check_answer(self, answer):
        correct = self.questions['Correct']
        if answer == correct:
            self.num_correct += 1
            self.flashcard.current_question_index = (self.flashcard.current_question_index + 1) % self.flashcard.get_num_questions()
        return answer == correct

    def get_current_question(self):
        return self.flashcard.get_question()

    def get_num_correct(self):
        return self.num_correct

    def previous_question(self):
        if self.flashcard.current_question_index == 0:
            return None
        self.flashcard.current_question_index -= 1
        
        return self.flashcard.get_question()
    
    def next_question(self):
        if self.flashcard.current_question_index == len(self.flashcard.questions) - 1:
            return None
        self.flashcard.current_question_index += 1

        return self.flashcard.get_question()




class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Your Cert Pocket Trainer")
        self.root.geometry("900x370")
        self.flashcard = Flashcard()
        self.quiz = Quiz()
        self.question_var = StringVar()
        self.answer_var = StringVar()
        self.question_label = tk.Label(self.root, text="Question: ")

        self.question_label.grid(row=0, column=0)

        self.answer_label = tk.Label(self.root, text="Answer: ")
        self.answer_label.grid(row=1, column=0)

        self.question_display = tk.Label(self.root, text="current question")
        self.question_display = tk.Text(self.root, width=100, height=25)

        self.question_display.grid(row=0, column=1)

        self.answer_display = tk.Label(self.root, text="")
        self.answer_display.grid(row=1, column=1)

        self.prev_button = tk.Button(
            self.root, text="Previous", command=self.previous_question)
        self.prev_button.grid(row=1, column=1)

        self.next_button = tk.Button(
            self.root, text="Next", command=self.next_question)
        self.next_button.grid(row=1, column=2)
        
        self.show_button = tk.Button(
            self.root, text="show_question", command=self.show_question)
        self.show_button.grid(row=1, column=0)
        
    def show_question(self):
        df = self.quiz.get_current_question()
        question = df.to_csv()
        print(question)
        self.question_display.insert(tk.END, '\n'+str(question))
        

        
    def check_answer(self):
        answer = self.answer_var.get()
        result = self.quiz.check_answer(answer)
        self.answer_var.set(result)
        print("checking Answer.......\n ", result)

    def next_question(self):
        next = self.quiz.next_question()
        self.show_question()
        print("next question.......\n ")
        
    def previous_question(self):
        self.quiz.previous_question()
        self.show_question()

    def run(self):
        self.root.mainloop()



