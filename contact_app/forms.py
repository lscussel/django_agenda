from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from contact_app.models import Contact

class ContactForm(forms.ModelForm):
  picture = forms.ImageField(
    widget=forms.FileInput(
      attrs={
        'accept': 'image/*',
        'required': False
      },
    ),
    required=False
  )
  # first_name = forms.CharField(
  #   widget=forms.TextInput(
  #     attrs={
  #       'class': 'classe-a classe-b',
  #       'placeholder': 'Aqui veio da sobrescrita da classe',
  #     }
  #   ),
  #   label='Primeiro Nome',
  #   help_text='Texto de ajuda para seu usuário',
  # )

  # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)

  #   self.fields['first_name'].widget.attrs.update(
  #     { 'placeholder': 'Aqui veio do init' },
  #   )

  class Meta:
    model = Contact
    fields = 'first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture',
    widgets = {}
    # widgets = {
    #   'first_name': forms.TextInput(
    #     attrs={
    #       'placeholder': 'Aqui veio do widget'
    #     }
    #   ),
    #   'last_name': forms.TextInput(
    #     attrs={
    #       'placeholder': 'Sobrenome'
    #     }
    #   ),
    # }

  def clean(self):
    # cleaned_data = self.cleaned_data
    # print(cleaned_data)
    # self.add_error(
    #   'first_name', ValidationError('Mensagem de erro', code='invalid')
    # )
    # self.add_error(
    #   None, ValidationError('Mensagem de erro non_field', code='invalid')
    # )

    cleaned_data = self.cleaned_data
    first_name = cleaned_data.get('first_name')
    last_name = cleaned_data.get('last_name')

    if first_name == last_name:
      self.add_error('last_name', ValidationError('Digite nomes diferentes para first name e last name', code='invalid'))

    return super().clean()
  
  def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name')
    # if first_name == 'ABC':
    #   raise ValidationError('Não digite ABC neste campo', code='invalid')

    # if first_name == 'ABC':
    #   self.add_error('first_name', ValidationError('Veio do add_error', code='invalid'))
    return first_name
  
class RegisterForm(UserCreationForm):
  first_name = forms.CharField(
    required=True,
    min_length=3
  )
  last_name = forms.CharField(
    required=True,
    min_length=3
  )
  email = forms.EmailField(
    required=True
  )

  class Meta:
    model = User
    fields = (
      'first_name', 'last_name', 'email',
      'username', 'password1', 'password2',
    )

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      self.add_error('email', ValidationError('Já existe este e-mail', code='invalid'))
    return email
  
class RegisterUpdateForm(forms.ModelForm):
  first_name = forms.CharField(
    min_length=2,
    max_length=30,
    required=True,
    help_text='Required',
    error_messages={
      'min-length': 'Please, add more than 2 letters'
    }
  )
  last_name = forms.CharField(
    min_length=2,
    max_length=30,
    required=True,
    help_text='Required',
  )
  password1 = forms.CharField(
    label='Senha',
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    help_text=password_validation.password_validators_help_text_html,
    required=False
  )
  password2 = forms.CharField(
    label='Confirmação de senha',
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    help_text='Use the same password as before',
    required=False
  )

  class Meta:
    model = User
    fields = (
      'first_name', 'last_name', 'email', 'username',
    )

  def save(self, commit=True):
    cleaned_data = self.cleaned_data
    user = super().save(commit=False)
    password = cleaned_data.get('password1')
    if password:
      user.set_password(password)
      
    if commit:
      user.save()


  def clean(self):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    if password1 or password2:
      if password1 != password2:
        self.add_error('password2', ValidationError('Senhas não batem', code='invalid'))
    return super().clean()


  def clean_email(self):
    email = self.cleaned_data.get('email')
    current_email = self.instance.email

    if email != current_email:
      if User.objects.filter(email=email).exists():
        self.add_error('email', ValidationError('Já existe este e-mail', code='invalid'))
    return email
    
    
  def clean_password1(self):
    password1 = self.cleaned_data.get('password1')
    if password1:
      try:
        password_validation.validate_password(password1)
      except ValidationError as errors:
        self.add_error('password1', ValidationError(errors))

    return password1