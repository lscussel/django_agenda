from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404, render, redirect
from contact_app.models import Contact

# Create your views here.
def index(request):
  contacts = Contact.objects.filter(show=True).order_by('-id')
  # print(contacts.query)
  paginator = Paginator(contacts, 10)  # Show 25 contacts per page.
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  context = {
    'page_obj': page_obj,
    'site_title': 'Contatos'
  }
  return render(request, 'contact_app/index.html', context)


def contact(request, contact_id):
  # o código single_contact = get_object_or_404(Contact.objects, pk=contact_id) faz o mesmo que as três linhas abaixo 
  # single_contact = Contact.objects.filter(pk=contact_id).first()
  # if single_contact is None:
  #   raise Http404
  single_contact = get_object_or_404(Contact.objects, pk=contact_id, show=True)
  contact_name = f'{single_contact.first_name} {single_contact.last_name}'
  context = {
    'contact': single_contact,
    'site_title': contact_name
  }
  return render(request, 'contact_app/contact.html', context)


def search(request):
  search_value = request.GET.get('q', '').strip()

  if search_value == '':
    return redirect('contact_app:index')

  contacts = Contact.objects.filter(show=True).filter(
    Q(first_name__icontains=search_value) |
    Q(last_name__icontains=search_value) |
    Q(phone__icontains=search_value) |
    Q(email__icontains=search_value)
  ).order_by('-id')
  paginator = Paginator(contacts, 10)  # Show 25 contacts per page.
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  context = {
    'page_obj': page_obj,
    'site_title': 'Search',
    'search_value': search_value,
  }
  return render(request, 'contact_app/index.html', context)