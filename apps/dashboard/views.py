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
            'prices': ['3449.49', '3134.45'] 
        }
        return JsonResponse(chart_data)