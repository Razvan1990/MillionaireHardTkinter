import random
import time
import tkinter
from tkinter import messagebox
import pygame
import os

import constans


class BuildSavelines(object):

    def __init__(self):
        self.letters = ["Q_A", "Q_B", "Q_C", "Q_D"]
        self._copied_letters = self.letters.copy()
        self.letters_to_values = {"A": 1, "B": 2, "C": 3, "D": 4}
        self.music_folder = os.path.join(os.getcwd(), "..", "wav")
        pygame.mixer.init()

    def get_phone_answer(self, dict_letter_label, button1, button2, button3, button4, button_safeline):
        # check how many buttons are completed
        phone_friend_sound = pygame.mixer.Sound(os.path.join(self.music_folder, "phone.wav"))
        phone_friend_sound.play()
        time.sleep(16)
        list_buttons = [button1, button2, button3, button4]
        list_available_letters = []
        if button1["text"] == "" or button2["text"] == "" or button3["text"] == "" or button4["text"] == "":
            # in this case we used 50 50 for this answer
            for button in list_buttons:
                if button["text"] != "":
                    list_available_letters.append(button["text"][0])  # first letter
            random_choose = random.randint(0, 1)
            if random_choose == 0:
                option = "Q_" + list_available_letters[0]
                message = f"I think the correct answer is {list_available_letters[0]}:\t{dict_letter_label[option]}"
            else:
                option = "Q_" + list_available_letters[1]
                message = f"I think the correct answer is {list_available_letters[1]}:\t{dict_letter_label[option]}"
            messagebox.showinfo(title="PHONE_ANSWER", message=message)
        else:
            random_chose = random.randint(0, len(self.letters) - 1)
            letter = self.letters[random_chose]
            message = f"I think the correct answer is {letter[2:]}:\t {dict_letter_label[letter]}"
            messagebox.showinfo(title="PHONE_ANSWER", message=message)
        button_safeline["state"] = tkinter.DISABLED
        button_safeline["bg"] = "#03102E"

    def make_fifty_fifty(self, dict_question, button1, button2, button3, button4, button_safeline):
        list_buttons = [button1, button2, button3, button4]
        dict_button_to_value = {"A": 1, "B": 2, "C": 3, "D": 4}
        correct_answer = dict_question[constans.LIST_NECESSARY_DICT[5]]
        # associate correct answer
        text_button = ""
        for letter in self.letters:
            if letter[2:] == correct_answer:
                # get the text from the button
                text_button = dict_question[constans.LIST_NECESSARY_DICT[dict_button_to_value[correct_answer]]]
                print(text_button)
                break
        # directly erase
        counter_erase = 0
        while True:
            random_button = random.randint(0, len(list_buttons) - 1)
            print(list_buttons[random_button]["text"][3:])
            if list_buttons[random_button]["text"][3:] != text_button:
                for letter in self.letters:
                    if list_buttons[random_button]["text"][0] == letter[-1]:
                        correct_removal = "Q_" + list_buttons[random_button]["text"][0]
                        self.letters.remove(correct_removal)
                list_buttons[random_button]["text"] = ""
                list_buttons.remove(list_buttons[random_button])
                counter_erase += 1
                '''
                need to update the list in case that we have 50/50 used and then to update in the other lifelines
                '''
                if counter_erase == 2:
                    break
        button_safeline["state"] = tkinter.DISABLED
        button_safeline["bg"] = "#03102E"

    def get_public_answers(self, button1, button2, button3, button4, button_safeline):
        '''
        we will generate four random values. We will find the max value and after that we will again randomly generate from 0 till 100-value and so on
        do not get to the same letter to A, we will use a dictionary probably and store a random letter to the value
        :return: a messagebox with some random values which should sum to 100
        '''
        max_rand1 = 0
        max_rand2 = 0
        max_rand3 = 0
        max_rand4 = 0
        list_buttons = [button1, button2, button3, button4]
        list_available_letters = []
        if button1["text"] == "" or button2["text"] == "" or button3["text"] == "" or button4["text"] == "":
            for button in list_buttons:
                if button["text"] != "":
                    list_available_letters.append(button["text"][0])  # first letter
            random1 = random.randint(0, 100)
            random2 = random.randint(0, 100)
            max_rand1 = self.get_max(random1, random2)
            if max_rand1 == 100:
                max_rand2 = 0
            else:
                max_rand2 = 100 - max_rand1
            # associate a value to a letter randomly

            number = random.randint(0, 1)
            if number == 0:
                message = f"The audience voted this way:\n{list_available_letters[0]}:\t{str(max_rand1)}\n{list_available_letters[1]}:\t{str(max_rand2)}"
            else:
                message = f"The audience voted this way:\n{list_available_letters[1]}:\t{str(max_rand2)}\n{list_available_letters[0]}:\t{str(max_rand1)}"
            messagebox.showinfo(title="VOTE", message=message)
        else:
            random1 = random.randint(0, 100)
            random2 = random.randint(0, 100)
            random3 = random.randint(0, 100)
            random4 = random.randint(0, 100)

            max_rand1 = self.get_max(random1, random2, random3, random4)
            # now check if it is not 100
            if max_rand1 == 100:
                max_rand2 = 0
                max_rand3 = 0
                max_rand4 = 0
            else:
                # appeal the function for 3 params, but make new generation
                random2 = random.randint(0, 100 - max_rand1)
                random3 = random.randint(0, 100 - max_rand1)
                random4 = random.randint(0, 100 - max_rand1)
                max_rand2 = self.get_max(random2, random3, random4)
                # check again
                if max_rand1 + max_rand2 == 100:
                    max_rand3 = 0
                    max_rand4 = 0
                else:
                    random3 = random.randint(0, 100 - max_rand1 - max_rand2)
                    random4 = random.randint(0, 100 - max_rand1 - max_rand2)
                    max_rand3 = self.get_max(random3, random4)
                    if max_rand1 + max_rand2 + max_rand3 == 100:
                        max_rand4 = 0
                    else:
                        max_rand4 = 100 - (max_rand1 + max_rand2 + max_rand3)

            list_values = [max_rand1, max_rand2, max_rand3, max_rand4]
            dict_results = self.create_random_picker_dict(self._copied_letters, list_values)
            # form the message
            message = f"The audience voted in this way:\nA:\t{dict_results["Q_A"]}%\nB:\t{dict_results["Q_B"]}%\nC:\t{dict_results["Q_C"]}%\nD:\t{dict_results["Q_D"]}%"
            messagebox.showinfo(title="VOTE", message=message)
        button_safeline["state"] = tkinter.DISABLED
        button_safeline["bg"] = "#03102E"

    def get_max(self, *args):
        if not args:
            return None
        return max(args)

    def create_random_picker_dict(self, list_letters, list_values):
        dict_chosen = {}
        for i in range(0, len(list_letters)):
            random_value = random.randint(0, len(list_letters) - 1)
            chosen_letter = list_letters[random_value]
            dict_chosen.update({chosen_letter: list_values[i]})
            # delete the chosen letter for letters
            list_letters.remove(chosen_letter)
        return dict_chosen
