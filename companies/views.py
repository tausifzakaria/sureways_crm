from django.shortcuts import render

# Create your views here.
def CompanyManagement(request):
    return render(request, 'companies.html')