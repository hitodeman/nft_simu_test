from django.urls import path

from . import views

urlpatterns = [
    path('calc_response',views.calc_response,name='calc_response'),
]