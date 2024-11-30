from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from workshop.forms import OnlineClientForm


def register(request):
    if request.method == 'POST':
        form = OnlineClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = OnlineClientForm()
    return render(request, 'workshop/register.html', {'form': form})