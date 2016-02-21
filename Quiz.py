import random
from abc import ABCMeta, abstractmethod


class MultipleChoiceQuestion:
    def __init__(self, element, correct_option, option_list):
        self.element = element
        self.correct_option = correct_option
        self.option_list = option_list


class Quiz:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.number_of_rounds = 0
        self.score = []

        # current
        self.current_question = None

    def getScore(self):
        return self.score

    @abstractmethod
    def generate_question(self):
        return None

    def update_score(self, correct):
        self.score.append(correct)

    def next_question(self):
        self.number_of_rounds += 1
        question = self.generate_question()
        return question


class ImageQuiz(Quiz):
    def __init__(self, elements_dict, options_dict, num_elements_quiz=4):
        super(ImageQuiz, self).__init__()
        self.elements_dict = elements_dict
        self.options_dict = options_dict
        self.num_elements_quiz = num_elements_quiz

        # Auxiliary attributes
        self.seen_elements_dict = dict()
        self.current_question = None

    def generate_question(self):
        '''
        Exaustive Algorithm. Shows all images until all are correct.
        :return: a multiple choice question
        '''
        if not self.elements_dict:
            if not self.seen_elements_dict:
                return False
            else:
                self.elements_dict = self.seen_elements_dict
                self.seen_elements_dict = dict()

        # 1. grab a key from the element_list randomly
        correct_key = random.choice(self.elements_dict.keys())

        # 2. Create a subset of the option_list for the quiz
        correct_element = self.elements_dict[correct_key]
        correct_option = self.options_dict[correct_key]
        quiz_options_list = list()
        quiz_options_list.append(correct_option)
        other_options = filter(lambda x: x != correct_option, set(self.options_dict.values()))
        quiz_options_list.extend(random.sample(other_options, self.num_elements_quiz - 1))

        # 3. Shuffle the new sub_option_list
        random.shuffle(quiz_options_list)
        question = MultipleChoiceQuestion({correct_key: correct_element}, correct_option, quiz_options_list)

        self.current_question = question
        return question

    def process_answer(self, question, correct):
        # update score
        self.update_score(correct)

        # 0. pop element from element list
        self.elements_dict.pop(question.element.keys()[0])

        if not correct:
            # save popped element in the seen_elements list
            self.seen_elements_dict.update(question.element)


class PainterQuiz(ImageQuiz):
    def __init__(self, element_list, option_list, num_elements_quiz=4):
        super(PainterQuiz, self).__init__(element_list, option_list, num_elements_quiz=num_elements_quiz)


class SaintQuiz(ImageQuiz):
    def __init__(self, element_list, option_list, num_elements_quiz=4):
        # Elements are Paintings and Options are saints
        super(SaintQuiz, self).__init__(element_list, option_list, num_elements_quiz=num_elements_quiz)