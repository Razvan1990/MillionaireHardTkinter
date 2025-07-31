import os
import random

import constans


class Reader(object):

    def __init__(self):
        #it is appealed in game folder
        self.text_file = os.path.join(os.getcwd(), "..", "QandA.txt")
        self.results_list = []
        # to check how to handle everything

    def read_and_create_necessary(self):
        with open(file=self.text_file, mode="r", encoding="utf-8") as game_file:
            lines = game_file.readlines()
            # get rid of new line character
            filtered_lines = list()
            for line in lines:
                if line != "\n":
                    filtered_lines.append(line[:-1])
            # create list for questions and list for answers
            questions = []
            answers = []
            for i in range(0, len(filtered_lines)):
                if i % 2 == 0:
                    questions.append(filtered_lines[i])
                else:
                    answers.append(filtered_lines[i])
            trimmed_answers = self.trim_answers(answers)
            self.extract_list_dicts(questions, trimmed_answers)
            # now choose one per prize
            game_list = self.choose_random_question_answer(self.results_list)
            print(game_list)
            return game_list

    @staticmethod
    def trim_answers(list_answers):
        list_trimmed = []
        for answer in list_answers:
            temp_list = []
            list_words = answer.split(",")
            # check to not have an extra space
            for word in list_words:
                if word.startswith(" "):
                    temp_list.append(word.lstrip())
                elif word.endswith(" "):
                    temp_list.append(word.rstrip())
                else:
                    temp_list.append(word)
            list_trimmed.append(temp_list)
        return list_trimmed

    def extract_list_dicts(self, list_questions, list_answers):
        '''
        :param list_answers:
        :param list_questions:
        :return: list_of_dicts
        In essennce we will have a list of dictionaries, in which the actual prize is the key and the values will be a list of dicts containing question, answers, correct answer
        [
        100: [
        {
            question:
            answers
            correct answer
        },
        .....
        ],
        200: [
        etc
        '''
        given_prices = self.extract_necessary_prizes(list_answers)
        # traverse through list of answers and where we find the value we will put as a dict
        for prize in given_prices:
            dict_prize_info = {}
            list_prizes = []  # list of dictionaries
            for i in range(0, len(list_answers)):
                if prize == int(list_answers[i][5]):
                    # create dict now
                    dict_prize = {}
                    dict_prize.update({constans.LIST_NECESSARY_DICT[0]: list_questions[i]})
                    dict_prize.update({constans.LIST_NECESSARY_DICT[1]: list_answers[i][0]})
                    dict_prize.update({constans.LIST_NECESSARY_DICT[2]: list_answers[i][1]})
                    dict_prize.update({constans.LIST_NECESSARY_DICT[3]: list_answers[i][2]})
                    dict_prize.update({constans.LIST_NECESSARY_DICT[4]: list_answers[i][3]})
                    dict_prize.update({constans.LIST_NECESSARY_DICT[5]: list_answers[i][4]})
                    list_prizes.append(dict_prize)
            dict_prize_info.update({prize: list_prizes})
            self.results_list.append(dict_prize_info)

    @staticmethod
    def extract_necessary_prizes(list_answers):
        given_prices = []
        for answer in list_answers:
            given_prices.append(int(answer[5]))
        given_prices.sort()
        # set puts in random place -> need to make a new list
        list_no_duplicates = []
        for prize in given_prices:
            if prize not in list_no_duplicates:
                list_no_duplicates.append(prize)
        return list_no_duplicates

    @staticmethod
    def choose_random_question_answer(list_dictionaries):
        list_game = []
        for list_dict in list_dictionaries:
            dict_q_game = {}
            for key in list_dict:
                # choose random value
                random_question = random.randint(0, len(list_dict[key]) - 1)
                dict_q_game.update({key: list_dict[key][random_question]})
            list_game.append(dict_q_game)
        return list_game
