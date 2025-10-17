from django.shortcuts import render

def login_view(request):
    # Renderiza la plantilla del login
    return render(request, "login/login.html")
