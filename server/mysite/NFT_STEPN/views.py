from django.http import JsonResponse
from .logic.api_test_new import output_result

# Create your views here.
def calc_response(response):
    return JsonResponse(output_result(),safe=False)