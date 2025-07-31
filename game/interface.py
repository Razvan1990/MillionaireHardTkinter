import os
import time

import pygame
import tkinter
from tkinter import *
from tkinter import messagebox

import constans
from game.safelines import BuildSavelines
from reader import Reader


class InterfaceCreator(object):

    def __init__(self):
        self.safeline = BuildSavelines()
        self.reader = Reader()
        self.my_question_list = self.reader.read_and_create_necessary()
        self.music_folder = os.path.join(os.getcwd(), "..", "wav")
        pygame.mixer.init()
        self.ico_image = os.path.join(os.getcwd(), "..", "million.ico")
        self.png_image = os.path.join(os.getcwd(), "..", "mil3.png")
        self.counter_questions = 0

    def create_game(self, window, image_canvas):
        global label_question
        global button_50
        global button_ask_audience
        global button_phone_friend
        global button_answer1
        global button_answer2
        global button_answer3
        global button_answer4

        question_id_price = list(self.my_question_list[self.counter_questions].keys())[
            0]  # this will resurn the prize -> debug to understand :)
        # frame.wm_withdraw()
        window.option_add('*Dialog.msg.font', 'Helvetica 18')
        # create canvas
        canvas = Canvas(window, height=750, width=1080, bg="#03102E", bd=0, relief=tkinter.GROOVE, highlightthickness=0,
                        highlightbackground="black")
        canvas.place(x=100, y=10)
        canvas.create_image((450, 325), image=image_canvas)
        # create a frame label for the questions and answers
        frame_QandA = LabelFrame(window, fg="#ffffff", bg="#03102E", font=("Helvetica", 15, "bold"), bd=5,
                                 cursor="target", width=1080, height=250, labelanchor="n",
                                 text="Who wants to be a millionaire",
                                 relief=tkinter.GROOVE)
        frame_QandA.place(x=100, y=700)
        # put labels and buttons
        label_question = Label(frame_QandA, text=self.my_question_list[self.counter_questions][question_id_price][
            constans.LIST_NECESSARY_DICT[0]], justify="right", anchor="ne",
                               font=("Helvetica", 14, "bold"),
                               cursor="star", fg="#ffffff", bg="#03102E")
        label_question.place(x=10, y=30)
        '''PUT BUTTONS'''
        button_answer1 = Button(frame_QandA,
                                text="A. " + self.my_question_list[self.counter_questions][question_id_price][
                                    constans.LIST_NECESSARY_DICT[1]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",  # lambda
                                )
        button_answer1.place(x=40, y=70)
        button_answer2 = Button(frame_QandA,
                                text="B. " + self.my_question_list[self.counter_questions][question_id_price][
                                    constans.LIST_NECESSARY_DICT[2]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",  # lambda
                                )
        button_answer2.place(x=630, y=70)
        button_answer3 = Button(frame_QandA,
                                text="C. " + self.my_question_list[self.counter_questions][question_id_price][
                                    constans.LIST_NECESSARY_DICT[3]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",  # lambda
                                )
        button_answer3.place(x=40, y=150)
        button_answer4 = Button(frame_QandA,
                                text="D. " + self.my_question_list[self.counter_questions][question_id_price][
                                    constans.LIST_NECESSARY_DICT[4]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",  # lambda
                                )
        button_answer4.place(x=630, y=150)
        # create lifeline buttons
        button_50 = Button(window, text="50:50", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                           font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                           relief=tkinter.GROOVE, highlightthickness=2,
                           command=lambda: self.safeline.make_fifty_fifty(
                               self.my_question_list[self.counter_questions][question_id_price], button_answer1,
                               button_answer2, button_answer3, button_answer4), )
        button_50.place(x=1190, y=120)
        button_ask_audience = Button(window, text="Public", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                                     font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                                     relief=tkinter.GROOVE, highlightthickness=2,
                                     command=lambda: self.safeline.get_public_answers(button_answer1, button_answer2,
                                                                                      button_answer3, button_answer4))
        button_ask_audience.place(x=1190, y=220)
        button_phone_friend = Button(window, text="Phone", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                                     font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                                     relief=tkinter.GROOVE, highlightthickness=2,
                                     command=lambda: self.safeline.get_phone_answer(
                                         self.my_question_list[self.counter_questions][question_id_price],
                                         button_answer1, button_answer2, button_answer3, button_answer4)
                                     )
        button_phone_friend.place(x=1190, y=320)

    def create_main_gui(self):
        global root
        # game_questions = self.reader.read_and_create_necessary()
        root = Tk()
        root.geometry("1280x960")
        root.resizable(NO, NO)
        root.iconbitmap(self.ico_image)
        root.title("Who wants to be a millionaire")
        image_canvas = PhotoImage(file=self.png_image)
        self.create_game(root, image_canvas)
        root["bg"] = "#03102E"
        root.mainloop()


if __name__ == "__main__":
    io = InterfaceCreator()
    io.create_main_gui()
