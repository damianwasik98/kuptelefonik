from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('observed', views.observed, name='observed'),
    path('api/price_chart_data', views.PhonePriceChartData.as_view(), name='price_chart_data')
]