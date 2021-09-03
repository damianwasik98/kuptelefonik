from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('observed', views.observed, name='observed'),
    path('follow/<int:phone_id>', views.follow, name='follow'),
    path('unfollow/<int:phone_id>', views.unfollow, name='unfollow'),
    path('api/price_chart_data', views.PhonePriceChartData.as_view(), name='price_chart_data'),
]