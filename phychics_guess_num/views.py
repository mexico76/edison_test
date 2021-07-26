from django.views.generic.base import View

from .services import get_vanga_list, make_choice,get_your_choice, check_result

class StartViev(View):
    def get(self, request):
        result = get_vanga_list(request)
        return result

    def post(self, request):
        result = make_choice(request)
        return result

class InputNumberView(View):
    def get(self, request):
        result = get_your_choice(request)
        return result

    def post(self, request):
        result = check_result(request)
        return result
