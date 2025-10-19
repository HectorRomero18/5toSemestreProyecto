from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View

class LoginView(View):
    template_name = 'airwrite/auth/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'error': 'Credenciales inválidas'})