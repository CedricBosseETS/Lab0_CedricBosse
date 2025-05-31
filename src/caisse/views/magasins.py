from django.shortcuts import render

def magasins_view(request):
    return render(request, 'magasins.html')
