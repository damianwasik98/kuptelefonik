from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('query')
    return render(request, 'search.html', {'query': query})

def observed(request):
    return render(request, 'observed.html')