from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Phone, ObservedPhone

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def search(request):
    query = request.GET.get('query')
    search_result = Phone.objects.filter(Q(name__icontains=query)) if query else []
    return render(request, 'search.html', {'query': query, 'results': search_result})

@login_required
def observed(request):
    observed_phones = ObservedPhone.get_user_observed_phones(user_id=request.user.id)

    from enum import Enum

    class PriceState(Enum):
        INCREASED = 0
        DECREASED = 1
        EQUAL = 2
        UNKNOWN = 3


    def format_price(price) -> str:
        if price is None:
            return ""
        return "{:.2f}".format(price)


    def price_state(current_price, observed_starting_price) -> bool:
        print(current_price, observed_starting_price)
        print(current_price == observed_starting_price)
        if not all([current_price, observed_starting_price]):
            return PriceState.UNKNOWN
        elif current_price > observed_starting_price:
            return PriceState.INCREASED
        elif current_price < observed_starting_price:
            return PriceState.DECREASED
        else:
            return PriceState.EQUAL

    phone_data = []
    for phone in observed_phones:
        current_lowest_price = phone.get_current_lowest_price()
        observed_starting_price = phone.get_observed_starting_price(user_id=request.user.id)
        price_s = price_state(current_lowest_price, observed_starting_price)

        data = {
            "phone": phone,
            "current_price": format_price(current_lowest_price),
            "old_price": format_price(observed_starting_price),
            "price_state": price_s
        }
        phone_data.append(data)
    
    return render(request, 'observed.html', {'phone_data': phone_data})

@login_required
def follow(request, phone_id):
    '''
    Adds phone into observed phones
    '''
    if request.method == 'POST':
        try:
            observed_obj = ObservedPhone.objects.get(phone_id=55, user_id=request.user.id)
        except ObjectDoesNotExist:
            pass
        else:
            ObservedPhone.follow(phone_id=phone_id, user_id=request.user.id)

    return HttpResponseRedirect('/dashboard/observed')

@login_required
def unfollow(request, phone_id):
    '''
    Removes followed phone
    '''
    if request.method == 'POST':
        ObservedPhone.unfollow(phone_id=phone_id, user_id=request.user.id)
    return HttpResponseRedirect('/dashboard/observed')

class PhonePriceChartData(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get_date_str(date):
        return date.strftime('%Y-%m-%d')

    def get(self, request, format=None):
        observed_phones = ObservedPhone.get_user_observed_phones(user_id=request.user.id)
        
        chart_data = {
            "chart_data": [
                {
                    "phone_id": phone.id,
                    'prices': [float(offer['price__min']) for offer in phone.get_all_lowest_offers()],
                    'dates': [self._get_date_str(offer['day']) for offer in phone.get_all_lowest_offers()]
                }
                for phone in observed_phones
            ]
        }
        return JsonResponse(chart_data)