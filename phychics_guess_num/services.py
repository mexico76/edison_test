from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from pynames.generators.russian import PaganNamesGenerator
import random

from phychics_guess_num.forms import NumberForm


class Phychic:
    def __init__(self, version_of_number = None, trust=0, try_count=0, all_versions = []):
        self.name = PaganNamesGenerator().get_name_simple()
        self.trust_level = trust
        self.version_of_number = version_of_number
        self.try_count = try_count
        self.all_versions = all_versions[:]

    def make_choice(self):
        '''Делаем попытку отгадать число загаданное пользоаптелем'''
        self.version_of_number = random.randint(10, 99)
        self.all_versions.append(self.version_of_number)

    def check_answer(self, user_answer):
        '''Проверка правильности данного ответа'''
        if user_answer==self.version_of_number:
            self.trust_level+=1
        else:
            self.trust_level-=1
        self.try_count+=1


def session_expired_decorator(func):
    def wrapper_func(request):
        if not 'vanga_ids' in request.session:
            vangas = tuple(Phychic() for __i in range(random.randint(2, 5)))
            request.session['vanga_ids'] = vangas
            request.session['user_history'] = []
            return HttpResponseRedirect(reverse('guess_num'))
        else:
           return func(request)
    return wrapper_func

@session_expired_decorator
def get_vanga_list(request):
    user_history = request.session['user_history']
    vangas = tuple(vanga for vanga in request.session['vanga_ids'])
    return render(request, 'phychics_guess_num/index.html', {'phychics': vangas, 'user_history': user_history})

@session_expired_decorator
def make_choice(request):
    vangas = tuple(vanga for vanga in request.session['vanga_ids'])
    tuple(vanga.make_choice() for vanga in vangas)
    return HttpResponseRedirect(reverse('write_num'))

@session_expired_decorator
def get_your_choice(request):
    number_form = NumberForm()
    user_history = request.session['user_history']
    vangas = tuple(vanga for vanga in request.session['vanga_ids'])
    return render(request, 'phychics_guess_num/your_number.html',
                  {'phychics': vangas, 'number_form': number_form, 'user_history': user_history})

@session_expired_decorator
def check_result(request):
    number_form = NumberForm(request.POST)
    vangas = tuple(vanga for vanga in request.session['vanga_ids'])
    if number_form.is_valid():
        tuple(vanga.check_answer(number_form.cleaned_data.get('number')) for vanga in vangas)
        request.session['user_history'].append(number_form.cleaned_data.get('number'))
        return HttpResponseRedirect(reverse('guess_num'))
    else:
        return HttpResponseRedirect(reverse('write_num'))