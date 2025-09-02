from django.shortcuts import render

# Create your views here.
def TaskManagement(request):
    return render(request, 'tasks.html')
