from contact_app.forms import RegisterForm, RegisterUpdateForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404, render, redirect
from contact_app.models import Contact

# Create your views here.
def register(request):
  form = RegisterForm()

  if request.method == 'POST':
    form = RegisterForm(request.POST)

    if form.is_valid():
      messages.success(request, 'Usuário registrado')
      form.save()
      return redirect('contact_app:index')

  context = {
    'form': form
  }
  return render(request, 'contact_app/register.html', context)

@login_required(login_url='contact_app:login')
def user_update(request):
  form = RegisterUpdateForm(instance=request.user)

  if request.method == 'POST':
    form = RegisterUpdateForm(instance=request.user, data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Usuário atualizado')
      return redirect('contact_app:login')
    messages.error(request, 'Usuário não atualizado')

  context = {
    'form': form
  }
  return render(request, 'contact_app/user_update.html', context)
  

def login_view(request):
  form = AuthenticationForm(request)

  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      auth.login(request, user)
      messages.success(request, 'Logaddo com sucesso!!')
      return redirect('contact_app:index')
    messages.error(request, 'Login inválido')

  context = {
    'form': form
  }
  return render(request, 'contact_app/login.html', context)


@login_required(login_url='contact_app:login')
def logout_view(request):
  auth.logout(request)
 
  return redirect('contact_app:login')
