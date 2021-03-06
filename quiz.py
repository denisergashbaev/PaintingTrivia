import random
from abc import ABCMeta, abstractmethod
from sqlalchemy.sql.expression import exists
from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from models.saint import Saint


class MultipleChoiceQuestion:
    def __init__(self, question, correct_answer, option_list):
        self.question_dict = question
        self.question = question.values()[0]
        self.correct_answer = correct_answer
        self.option_list = option_list


class Quiz:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.number_of_rounds = 0
        self.score = []

        # current
        self.current_question = None

        self.right_guesses = 0
        self.wrong_guesses = 0

    @abstractmethod
    def generate_question(self):
        return

    def update_score(self, correct):
        if correct:
            self.right_guesses += 1
        else:
            self.wrong_guesses += 1
        self.score.append(correct)

    def next_question(self):
        self.number_of_rounds += 1
        question = self.generate_question()
        return question


class ImageQuiz(Quiz):
    def __init__(self, num_elements_quiz=4):
        super(ImageQuiz, self).__init__()

        self.elements_dict, self.options_dict = self.initialize_image_quiz(num_elements=10)
        self.num_elements_quiz = num_elements_quiz

        self.seen_elements_dict = dict()
        self.current_question = None

    @abstractmethod
    def initialize_image_quiz(self, num_elements):
        return

    def generate_question(self):
        '''
        Exhaustive Algorithm. Shows all images until all are correct.
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
        correct_option = self.options_dict[correct_key]
        quiz_options = random.sample(set(self.options_dict.values()) - set([correct_option]), self.num_elements_quiz - 1)
        quiz_options.append(correct_option)

        # 3. Shuffle the new sub_option_list
        random.shuffle(quiz_options)
        question = MultipleChoiceQuestion({correct_key: self.elements_dict[correct_key]}, correct_option, quiz_options)

        self.current_question = question
        return question

    def process_answer(self, answer):
        correct = answer == self.current_question.correct_answer.id

        # update score
        self.update_score(correct)

        # 0. pop element from element list
        self.elements_dict.pop(self.current_question.question_dict.keys()[0])

        if not correct:
            # save popped element in the seen_elements list
            self.seen_elements_dict.update(self.current_question.question_dict)


class PainterQuiz(ImageQuiz):
    def __init__(self, num_elements_quiz=4):
        super(PainterQuiz, self).__init__(num_elements_quiz=num_elements_quiz)

    def initialize_image_quiz(self, num_elements=5):
        stmt = exists().where(Painter.id == Painting.painter_id)
        selected_painters = Painter.query.filter(stmt).order_by(func.random()).limit(num_elements).all()

        painters_dict = dict()
        paintings_dict = dict()
        selected_paintings = []
        for key, painter in enumerate(selected_painters):
            painting = Painting.query.filter(Painting.painter_id == painter.id).order_by(func.random()).limit(
                1).first()
            selected_paintings.append(painting)
            painters_dict[key] = painter
            paintings_dict[key] = painting
        return paintings_dict, painters_dict


class SaintQuiz(ImageQuiz):
    def __init__(self, num_elements_quiz=4):
        # Elements are Paintings and Options are saints
        super(SaintQuiz, self).__init__(num_elements_quiz=num_elements_quiz)

    def initialize_image_quiz(self, num_elements=5):
        selected_saints = Saint.query.filter(Saint.paintings.any()).order_by(func.random()).limit(num_elements).all()

        saints_dict = dict()
        paintings_dict = dict()
        selected_paintings = []
        for key, saint in enumerate(selected_saints):
            painting = Painting.query.filter(Painting.saints.any(id=saint.id)).order_by(func.random()).limit(
                1).first()
            selected_paintings.append(painting)
            saints_dict[key] = saint
            paintings_dict[key] = painting
        return paintings_dict, saints_dict
