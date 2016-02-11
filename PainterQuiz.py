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
    def __init__(self, element_list, option_list, related_attributes=["painter_id", "id"], num_elements_quiz=4):
        super(ImageQuiz, self).__init__()
        self.element_list = element_list
        self.option_list = option_list
        self.related_attributes = related_attributes
        self.num_elements_quiz = num_elements_quiz

        # Auxiliary attributes
        self.seen_elements = []
        self.current_question = None

    def generate_question(self):
        '''
        Exaustive Algorithm. Shows all images until all are correct.
        :return: a multiple choice question
        '''
        if not self.element_list:
            if not self.seen_elements:
                return False
            else:
                self.element_list = self.seen_elements
                self.seen_elements = []

        # 1. grab an element from the element_list randomly
        correct_element = random.choice(self.element_list)

        # 2. Create a subset of the option_list for the quiz
        quiz_option_list = []

        #   - get its corresponding option that should also exist in the option_list
        correct_option_attr = self.get_option_attr_from_element(correct_element)
        correct_option = filter(lambda x: self.get_element_attr_from_option(x) == correct_option_attr, self.option_list)

        quiz_option_list.extend(correct_option)

        #   - get m-1 other options different from the corresponding option
        other_options = random.sample(
            set(list(filter(lambda x: self.get_element_attr_from_option(x) != correct_option_attr, self.option_list))),
            self.num_elements_quiz - 1
        )
        quiz_option_list.extend(other_options)

        # 3. Shuffle the new sub_option_list
        random.shuffle(quiz_option_list)

        question = MultipleChoiceQuestion(correct_element, correct_option[0], quiz_option_list)

        self.current_question = question
        return question

    def process_answer(self, question, correct):
        # update score
        self.update_score(correct)

        # 0. pop element from element list
        self.element_list.remove(question.element)

        if not correct:
            # save popped element in the seen_elements list
            self.seen_elements.append(question.element)

    def get_option_attr_from_element(self, element):
        attribute_name = self.related_attributes[0]
        if attribute_name is not "":
            option_attr = getattr(element, attribute_name)
            return option_attr

    def get_element_attr_from_option(self, option):
        attribute_name = self.related_attributes[1]
        if attribute_name is not "":
            element_attr = getattr(option, attribute_name)
            return element_attr
