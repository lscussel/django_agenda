from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from contact_app.forms import ContactForm
from contact_app.models import Contact


@login_required(login_url='contact_app:login')
def create(request):
  form_action = reverse('contact_app:create')

  if request.method == 'POST':
    form = ContactForm(request.POST, request.FILES)

    if form.is_valid():
      # contact = form.save(commit=False)
      # contact.show = False
      # contact.save()
      contact = form.save(commit=False)
      contact.owner = request.user
      contact.save()
      return redirect('contact_app:update', contact_id=contact.id)

    context = {
      'form': form,
      'form_action': form_action
    }
    return render(request, 'contact_app/create.html', context)

  form = ContactForm()
  context = {
    'form': form,
    'form_action': form_action
  }
  return render(request, 'contact_app/create.html', context)


@login_required(login_url='contact_app:login')
def update(request, contact_id):
  contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
  form_action = reverse('contact_app:update', args=(contact_id, ))

  if request.method == 'POST':
    form = ContactForm(request.POST, request.FILES, instance=contact)

    if form.is_valid():
      contact = form.save()
      return redirect('contact_app:update', contact_id=contact.id)

    context = {
      'form': form,
      'form_action': form_action
    }
    return render(request, 'contact_app/create.html', context)

  form = ContactForm(instance=contact)
  context = {
    'form': form,
    'form_action': form_action
  }
  return render(request, 'contact_app/create.html', context)


@login_required(login_url='contact_app:login')
def delete(request, contact_id):
  contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
  confirmation = request.POST.get('confirmation', 'no')
  if confirmation == 'yes':
    contact.delete()
    return redirect('contact_app:index')
  
  context = {
    'contact': contact,
    'confirmation': confirmation
  }
  return render(request, 'contact_app/contact.html', context)

