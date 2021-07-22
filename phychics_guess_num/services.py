from pynames.generators.russian import PaganNamesGenerator
import random

class Phychic:
    def __init__(self, version_of_number = None, trust=0, try_count=0, all_versions = []):
        self.name = PaganNamesGenerator().get_name_simple()
        self.trust_level = trust
        self.version_of_number = version_of_number
        self.try_count = try_count
        self.all_versions = all_versions[:]

    def make_choice(self):
        '''Делаем попытку отгадать число загаданное пользоаптелем'''
        self.version_of_number = random.randint(0, 100) # пока до 100
        self.all_versions.append(self.version_of_number)

    def check_answer(self, user_answer):
        '''Проверка правильности данного ответа'''
        if user_answer==self.version_of_number:
            self.trust_level+=1
        else:
            self.trust_level-=1
        self.try_count+=1


