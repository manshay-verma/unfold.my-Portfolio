from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'portfolio/base.html')

def portfolio_single(request, name):
    return render(request, f'portfolio/{name}.html')