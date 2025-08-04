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
        self.dict_counter_prizes = {0: 100, 1: 200, 2: 300, 3: 500, 4: 1000, 5: 1500, 6: 2500, 7: 5000, 8: 7500,
                                    9: 10000, 10: 15000, 11: 25000, 12: 50000, 13: 75000, 14: 100000}
        self.question_id_price = list(self.my_question_list[self.counter_questions].keys())[0]

    def compute_wrong_answer(self, amount, button_pressed, response, list_buttons, question_id_price):
        wrong_answer = pygame.mixer.Sound(os.path.join(self.music_folder, "wrong.wav"))
        wrong_answer.play()
        messagebox.showinfo(title="WRONG ANSWER",
                            message=f"Sorry, wrong answer! Unfortunately you have won just {str(amount)} RON\n")
        # color your answer red, correct answer green and make all buttons disabled
        button_50["state"] = tkinter.DISABLED
        button_ask_audience["state"] = tkinter.DISABLED
        button_phone_friend["state"] = tkinter.DISABLED
        button_answer1["state"] = tkinter.DISABLED
        button_answer2["state"] = tkinter.DISABLED
        button_answer3["state"] = tkinter.DISABLED
        button_answer4["state"] = tkinter.DISABLED
        button_walkaway["state"] = tkinter.DISABLED
        # color red
        button_pressed["bg"] = "#E33B17"
        # colore green
        for keys in self.my_question_list[self.counter_questions][question_id_price]:
            if keys[2:] == response:
                # we now that there will be a single correct response -> list[0]
                correct_answer_label = [button for button in list_buttons if button["text"].startswith(response)][0]
                print(correct_answer_label)
                correct_answer_label["bg"] = "#1F9413"
                return

    def play_game(self, button_pressed, list_buttons, list_labels):
        # first we will ask the contestant to be sure if that is the correct answer
        option = messagebox.askquestion(title="FINAL ANSWER", message="Do you want to block your answer")
        if option == "no":
            return
        # get text of button pressed
        text = button_pressed["text"]
        '''start checking'''
        self.question_id_price = list(self.my_question_list[self.counter_questions].keys())[0]
        response = ""
        for keys in self.my_question_list[self.counter_questions][self.question_id_price]:
            if keys == "R":
                response = self.my_question_list[self.counter_questions][self.question_id_price][keys]
                print(response)
                break
        '''check response'''
        if text[:1] != response:
            # we need first to check at what value is our counter
            # 1. 1000 won
            if self.counter_questions >= 4 and self.counter_questions < 9:
                self.compute_wrong_answer(1000, button_pressed, response, list_buttons, self.question_id_price)
            elif self.counter_questions >= 9:
                self.compute_wrong_answer(10000, button_pressed, response, list_buttons, self.question_id_price)
            else:
                self.compute_wrong_answer(0, button_pressed, response, list_buttons, self.question_id_price)
        else:
            correct_answer = pygame.mixer.Sound(os.path.join(self.music_folder, "correct.wav"))
            correct_answer.play()
            messagebox.showinfo(title="CORRECT",
                                message="Congratulations! The response is correct.Let's go the the next question")
            for keys in self.my_question_list[self.counter_questions][self.question_id_price]:
                if keys[2:] == response:
                    # we now that there will be a single correct response -> list[0]
                    correct_answer_label = [button for button in list_buttons if button["text"].startswith(response)][0]
                    correct_answer_label["bg"] = "#1F9413"
            self.counter_questions += 1
            # check if we won 1 miliion
            if self.counter_questions > 14:
                # you are a milionaire
                millionaire = pygame.mixer.Sound(os.path.join(self.music_folder, "million_winner.wav"))
                millionaire.play()
                button_50["state"] = tkinter.DISABLED
                button_ask_audience["state"] = tkinter.DISABLED
                button_phone_friend["state"] = tkinter.DISABLED
                button_answer1["state"] = tkinter.DISABLED
                button_answer2["state"] = tkinter.DISABLED
                button_answer3["state"] = tkinter.DISABLED
                button_answer4["state"] = tkinter.DISABLED
                button_walkaway["state"] = tkinter.DISABLED
            else:
                # now we need to go to the next question
                time.sleep(3)
                label_question.config(text="")
                button_answer1["text"] = ""
                button_answer2["text"] = ""
                button_answer3["text"] = ""
                button_answer4["text"] = ""
                button_answer1["bg"] = "#03102E"
                button_answer2["bg"] = "#03102E"
                button_answer3["bg"] = "#03102E"
                button_answer4["bg"] = "#03102E"
                self.question_id_price = list(self.my_question_list[self.counter_questions].keys())[0]
                label_question["text"] = self.my_question_list[self.counter_questions][self.question_id_price][
                    constans.LIST_NECESSARY_DICT[0]]
                button_answer1["text"] = "A. " + self.my_question_list[self.counter_questions][self.question_id_price][
                    constans.LIST_NECESSARY_DICT[1]]
                button_answer2["text"] = "B. " + self.my_question_list[self.counter_questions][self.question_id_price][
                    constans.LIST_NECESSARY_DICT[2]]
                button_answer3["text"] = "C. " + self.my_question_list[self.counter_questions][self.question_id_price][
                    constans.LIST_NECESSARY_DICT[3]]
                button_answer4["text"] = "D. " + self.my_question_list[self.counter_questions][self.question_id_price][
                    constans.LIST_NECESSARY_DICT[4]]
                # update the label at which question we are
                for label in list_labels:
                    if label["text"] == str(self.dict_counter_prizes[self.counter_questions]):
                        label["bg"] = "#DE8414"
                    else:
                        label["bg"] = "#03102E"

    def walk_away(self, list_buttons):
        # we will just check depending on where the counter is - create a dictionary counter-prize
        if self.counter_questions == 0:
            messagebox.showinfo(title="NO LOSE", message="You are not losing anything. You don't need to quit!")
            return
        else:
            amount_won = self.dict_counter_prizes[self.counter_questions - 1]
            message = f"Congratulations you have won a check of {amount_won} !\n Let's ask the computer to show us the correct response...."
            messagebox.showinfo(title="CONGRATS", message=message)
            # make all buttons unavailable
            button_50["state"] = tkinter.DISABLED
            button_ask_audience["state"] = tkinter.DISABLED
            button_phone_friend["state"] = tkinter.DISABLED
            button_answer1["state"] = tkinter.DISABLED
            button_answer2["state"] = tkinter.DISABLED
            button_answer3["state"] = tkinter.DISABLED
            button_answer4["state"] = tkinter.DISABLED
            button_walkaway["state"] = tkinter.DISABLED
            # check what is the correct answer
            question_id_price = list(self.my_question_list[self.counter_questions].keys())[0]
            response = ""
            for keys in self.my_question_list[self.counter_questions][question_id_price]:
                if keys == "R":
                    response = self.my_question_list[self.counter_questions][question_id_price][keys]
                    print(response)
                    break
            for keys in self.my_question_list[self.counter_questions][question_id_price]:
                if keys[2:] == response:
                    # we now that there will be a single correct response -> list[0]
                    correct_answer_label = [button for button in list_buttons if button["text"].startswith(response)][0]
                    time.sleep(2)
                    correct_answer_label["bg"] = "#1F9413"
                    return

    def create_game(self, window, image_canvas):
        global label_question
        global button_50
        global button_ask_audience
        global button_phone_friend
        global button_answer1
        global button_answer2
        global button_answer3
        global button_answer4
        global button_walkaway

        # labels
        global label_100
        global label_200
        global label_300
        global label_500
        global label_1000
        global label_1500
        global label_2500
        global label_5000
        global label_7500
        global label_10000
        global label_15000
        global label_25000
        global label_50000
        global label_75000
        global label_100000

        # start game music
        start_game_sound = pygame.mixer.Sound(os.path.join(self.music_folder, "start.wav"))
        start_game_sound.play()

        # this will resurn the prize -> debug to understand :)
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
        label_question = Label(frame_QandA, text=self.my_question_list[self.counter_questions][self.question_id_price][
            constans.LIST_NECESSARY_DICT[0]], justify="right", anchor="ne",
                               font=("Helvetica", 14, "bold"),
                               cursor="star", fg="#ffffff", bg="#03102E")
        label_question.place(x=10, y=30)
        '''PUT BUTTONS'''
        button_answer1 = Button(frame_QandA,
                                text="A. " + self.my_question_list[self.counter_questions][self.question_id_price][
                                    constans.LIST_NECESSARY_DICT[1]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",
                                command=lambda: self.play_game(button_answer1, list_buttons, list_prize_labels)
                                )
        button_answer1.place(x=40, y=70)
        button_answer2 = Button(frame_QandA,
                                text="B. " + self.my_question_list[self.counter_questions][self.question_id_price][
                                    constans.LIST_NECESSARY_DICT[2]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",
                                command=lambda: self.play_game(button_answer2, list_buttons, list_prize_labels)
                                )
        button_answer2.place(x=630, y=70)
        button_answer3 = Button(frame_QandA,
                                text="C. " + self.my_question_list[self.counter_questions][self.question_id_price][
                                    constans.LIST_NECESSARY_DICT[3]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",
                                command=lambda: self.play_game(button_answer3, list_buttons, list_prize_labels)
                                )
        button_answer3.place(x=40, y=150)
        button_answer4 = Button(frame_QandA,
                                text="D. " + self.my_question_list[self.counter_questions][self.question_id_price][
                                    constans.LIST_NECESSARY_DICT[4]], width=32, height=2, fg="#ffffff", bg="#03102E",
                                font=("Helvetica", 14, "bold"), cursor="star",
                                command=lambda: self.play_game(button_answer4, list_buttons, list_prize_labels)
                                )
        button_answer4.place(x=630, y=150)
        list_buttons = [button_answer1, button_answer2, button_answer3, button_answer4]
        # create lifeline buttons
        button_50 = Button(window, text="50:50", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                           font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                           relief=tkinter.GROOVE, highlightthickness=2,
                           command=lambda: self.safeline.make_fifty_fifty(
                               self.my_question_list[self.counter_questions][self.question_id_price], button_answer1,
                               button_answer2, button_answer3, button_answer4, button_50), )
        button_50.place(x=1190, y=120)
        button_ask_audience = Button(window, text="Public", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                                     font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                                     relief=tkinter.GROOVE, highlightthickness=2,
                                     command=lambda: self.safeline.get_public_answers(button_answer1, button_answer2,
                                                                                      button_answer3, button_answer4,
                                                                                      button_ask_audience))
        button_ask_audience.place(x=1190, y=220)
        button_phone_friend = Button(window, text="Phone", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                                     font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                                     relief=tkinter.GROOVE, highlightthickness=2,
                                     command=lambda: self.safeline.get_phone_answer(
                                         self.my_question_list[self.counter_questions][self.question_id_price],
                                         button_answer1, button_answer2, button_answer3, button_answer4,
                                         button_phone_friend)
                                     )
        button_phone_friend.place(x=1190, y=320)
        button_walkaway = Button(window, text="Quit", width=6, height=3, fg="#ffffff", bg="#C95D0E",
                                 font=("Helvetica", 14, "bold"), cursor="star", bd=3, highlightbackground="red",
                                 relief=tkinter.GROOVE, highlightthickness=2,
                                 command=lambda: self.walk_away(list_buttons))
        button_walkaway.place(x=1190, y=420)
        # put labels
        label_100 = Label(window, text="100", justify="center",
                          font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#ffffff", bg="#DE8414", width=9, height=2)
        label_100.place(x=5, y=650)
        label_200 = Label(window, text="200", justify="center",
                          font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_200.place(x=5, y=610)
        label_300 = Label(window, text="300", justify="center",
                          font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_300.place(x=5, y=570)
        label_500 = Label(window, text="500", justify="center",
                          font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_500.place(x=5, y=530)
        label_1000 = Label(window, text="1000", justify="center",
                           font=("Helvetica", 11, "bold"),
                           cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_1000.place(x=5, y=490)
        # second threshold
        label_1500 = Label(window, text="1500", justify="center",
                           font=("Helvetica", 11, "bold"),
                           cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_1500.place(x=5, y=450)
        label_2500 = Label(window, text="2500", justify="center",
                           font=("Helvetica", 11, "bold"),
                           cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_2500.place(x=5, y=410)
        label_5000 = Label(window, text="5000", justify="center",
                           font=("Helvetica", 11, "bold"),
                           cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_5000.place(x=5, y=370)
        label_7500 = Label(window, text="7500", justify="center",
                           font=("Helvetica", 11, "bold"),
                           cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_7500.place(x=5, y=330)
        label_10000 = Label(window, text="10000", justify="center",
                            font=("Helvetica", 11, "bold"),
                            cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_10000.place(x=5, y=280)
        # third threshold
        label_15000 = Label(window, text="15000", justify="center",
                            font=("Helvetica", 11, "bold"),
                            cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_15000.place(x=5, y=230)
        label_25000 = Label(window, text="25000", justify="center",
                            font=("Helvetica", 11, "bold"),
                            cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_25000.place(x=5, y=180)
        label_50000 = Label(window, text="50000", justify="center",
                            font=("Helvetica", 11, "bold"),
                            cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_50000.place(x=5, y=130)
        label_75000 = Label(window, text="75000", justify="center",
                            font=("Helvetica", 11, "bold"),
                            cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_75000.place(x=5, y=80)
        label_100000 = Label(window, text="100000", justify="center",
                             font=("Helvetica", 11, "bold"),
                             cursor="star", fg="#ffffff", bg="#03102E", width=9, height=2)
        label_100000.place(x=5, y=30)
        list_prize_labels = [label_100, label_200, label_300, label_500, label_1000, label_1500, label_2500, label_5000,
                             label_7500, label_10000, label_15000, label_25000, label_50000, label_75000, label_100000]
        if self.counter_questions == 14:
            last_question = pygame.mixer.Sound(os.path.join(self.music_folder, "final_question.wav"))
            last_question.play()

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
