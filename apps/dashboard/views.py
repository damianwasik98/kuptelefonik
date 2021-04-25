from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('query')
    return render(request, 'search.html', {'query': query})

def observed(request):
    return render(request, 'observed.html')

class PhonePriceChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        chart_data = {
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
        return JsonResponse(chart_data)