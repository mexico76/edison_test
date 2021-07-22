from django.urls import path
from .views import StartViev, InputNumberView

urlpatterns = [
    path('', StartViev.as_view(), name='guess_num'),
    path('input_number', InputNumberView.as_view(), name='write_num'),
]
