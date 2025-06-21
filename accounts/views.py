from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Cliente
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('listar_productos')
        else:
            return render(request, 'accounts/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nombre = request.POST['nombre']
        correo = request.POST['correo']

    
        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ El nombre de usuario ya está registrado.')
            return redirect('registro')

      
        user = User.objects.create_user(username=username, password=password)
        Cliente.objects.create(user=user, nombre=nombre, correo=correo)

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '✅ Usuario registrado y sesión iniciada.')
            return redirect('listar_productos')
        else:
            messages.warning(request, 'Cuenta creada, pero no se pudo iniciar sesión.')

    return render(request, 'accounts/registro.html')