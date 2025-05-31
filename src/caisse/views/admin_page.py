from django.shortcuts import render

def admin_view(request):
    return render(request, 'admin.html')
