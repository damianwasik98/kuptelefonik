from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from .models import Phone

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('query')
    search_result = Phone.objects.all()
    return render(request, 'search.html', {'query': query, 'results': search_result})

def observed(request):
    observed_phones = Phone.objects.filter(observed=True)
    return render(request, 'observed.html', {'observed_phones': observed_phones})

class PhonePriceChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        phone_id = int(request.GET.get('phone_id'))
        if phone_id == 1:
            chart_data = {
                "phone_id": phone_id,
                'prices': [
                    "4449.99",
                    "4149.99",
                    "4449.99",
                    "4449.99",
                    "4449.99",
                    "4449.99",
                    "4249.99",
                ],
                'dates': [
                    '5 miesięcy temu',
                    '4 miesiące temu',
                    '3 miesiące temu',
                    '2 miesiące temu',
                    '1 miesiąc temu',
                    '14 dni temu',
                    '2 dni temu'
                ]
            }
        else:
            chart_data = {
                "phone_id": phone_id,
                'prices': [
                    "3649.99",
                    "3649.99",
                    "3649.99",
                    "3199.99",
                    "3449.99",
                    "3449.99",
                    "3449.99",
                ],
                'dates': [
                    '5 miesięcy temu',
                    '4 miesiące temu',
                    '3 miesiące temu',
                    '2 miesiące temu',
                    '1 miesiąc temu',
                    '14 dni temu',
                    '2 dni temu'
                ]
            }
        return JsonResponse(chart_data)