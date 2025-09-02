from django.shortcuts import render

# Create your views here.
def ContactManagement(request):
    return render(request, 'contacts.html')
