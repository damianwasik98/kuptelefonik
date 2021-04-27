from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView

from .models import Phone, Offer

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

def follow(request, phone_id):
    '''
    Adds phone into observed phones
    '''
    if request.method == 'POST':
        phone = get_object_or_404(Phone, id=phone_id)
        phone.follow()
    return HttpResponseRedirect('/dashboard/observed')

def unfollow(request, phone_id):
    '''
    Removes followed phone
    '''
    if request.method == 'POST':
        phone = get_object_or_404(Phone, id=phone_id)
        phone.unfollow()
    return HttpResponseRedirect('/dashboard/observed')

class PhonePriceChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        observed_phones = Phone.get_observed()
        
        chart_data = {
            "chart_data": [
                {
                    "phone_id": phone.id,
                    'prices': [str(offer.price) for offer in phone.get_all_offers()],
                    'dates': [offer.get_date_str() for offer in phone.get_all_offers()]
                }
                for phone in observed_phones
            ]
        }
        return JsonResponse(chart_data)