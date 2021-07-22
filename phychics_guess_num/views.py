import ctypes

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
import random
from .services import Phychic
from .forms import NumberForm

class StartViev(View):
    def get(self, request):
        if request.session.session_key is None or not 'vanga_ids' in request.session:
            vangas = list( Phychic() for __i in range(random.randint(2, 5)))
            request.session['vanga_ids'] = list(id(vanga) for vanga in vangas)
        else:
            vangas = list(ctypes.cast(vanga, ctypes.py_object).value for vanga in request.session['vanga_ids'])
        return render(request, 'phychics_guess_num/index.html', {'phychics': vangas})

    def post(self, request):
        phychics = list(ctypes.cast(vanga, ctypes.py_object).value for vanga in request.session['vanga_ids'])
        list(vanga.make_choice() for vanga in phychics)
        return HttpResponseRedirect(reverse('write_num',))

class InputNumberView(View):
    def get(self, request):
        if 'vanga_ids' in request.session:
            number_form = NumberForm()
            phychics = list(ctypes.cast(vanga, ctypes.py_object).value for vanga in request.session['vanga_ids'])
            return render(request, 'phychics_guess_num/your_number.html', {'phychics': phychics, 'number_form':number_form})
        else:
            return HttpResponseRedirect(reverse('guess_num', ))

    def post(self, request):
        number_form = NumberForm(request.POST)
        phychics = list(ctypes.cast(vanga, ctypes.py_object).value for vanga in request.session['vanga_ids'])
        if number_form.is_valid():
            list(vanga.check_answer(number_form.cleaned_data.get('number')) for vanga in phychics)
        # phychics = list(vanga.check_answer for vanga in phychics)
        return HttpResponseRedirect(reverse('guess_num',))

