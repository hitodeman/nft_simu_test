from django.http import JsonResponse
from requests import request
from .logic.api_test_new import output_result

# Create your views here.
def calc_response(response):
    if response.method == 'GET':
        return JsonResponse(output_result(),safe=False)
    else:
        return JsonResponse(output_result(
            request.POST.get('initial_cost_SOL'),
            request.POST.get('j_rate_static_flg'),
            request.POST.getlist('lvUp_setting'),
            request.POST.get('type'),
            request.POST.get('calc_range'),
            request.POST.getlist('j_rate'),
            request.POST.get('level'),
            request.POST.get('quality'),
            request.POST.getlist('NumOfSneakers'),
            request.POST.getlist('Sneakers_initial_attr'),
            request.POST.get('accum_gst')
        ),safe=False)