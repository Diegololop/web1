from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'duration', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=200, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='client',
                phone=self.cleaned_data['phone']
            )
            Client.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone']
            )
        return user

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=[('mechanic', 'Mecánico'), ('receptionist', 'Recepcionista')])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(max_length=150, required=True, label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Contraseña')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
            self.fields['username'].disabled = True  # Username can't be changed
            self.fields['password'].required = False

    def save(self, commit=True):
        client = super().save(commit=False)
        
        if not client.pk:  # New client
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            client.user = user
            UserProfile.objects.create(
                user=user,
                role='client',
                phone=self.cleaned_data['phone']
            )
        else:  # Existing client
            user = client.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            
            user_profile = user.userprofile
            user_profile.phone = self.cleaned_data['phone']
            user_profile.save()
        
        if commit:
            client.save()
        
        return client
    
class EmployeeCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=15, required=True, label='Teléfono')
    role = forms.ChoiceField(
        choices=[('mechanic', 'Mecánico'), ('receptionist', 'Recepcionista')],
        label='Cargo'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone']
            )
        return user
    
from datetime import datetime, timedelta
from django.utils import timezone
    
class ReservationForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Detalles adicionales de la reserva...'
        })
    )

    # Campos para usuarios no autenticados
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['service', 'date', 'time', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa brevemente el problema o servicio requerido'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if not self.user or not self.user.is_authenticated:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True
            self.fields['phone'].required = True

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        service = cleaned_data.get('service')

        if date and time and service:
            # Combinar fecha y hora
            datetime_start = timezone.make_aware(
                datetime.combine(date, time)
            )
            
            # Validar horario de trabajo (9:00 - 18:00)
            if time.hour < 9 or time.hour >= 18:
                raise forms.ValidationError(
                    'Las reservas solo están disponibles entre las 9:00 y 18:00'
                )

            # Validar que la fecha no sea en el pasado
            if datetime_start < timezone.now():
                raise forms.ValidationError(
                    'No se pueden hacer reservas en el pasado'
                )

            # Calcular tiempo de finalización (duración del servicio + 10 min)
            service_duration = timedelta(minutes=service.duration)
            buffer_time = timedelta(minutes=10)
            datetime_end = datetime_start + service_duration + buffer_time

            # Verificar si hay otras reservas que se solapan
            overlapping_reservations = Reservation.objects.filter(
                service_date__lt=datetime_end,
                service_date__gt=datetime_start - service_duration - buffer_time
            )

            if overlapping_reservations.exists():
                raise forms.ValidationError(
                    'El horario seleccionado no está disponible. Por favor, elija otro horario.'
                )

            cleaned_data['service_date'] = datetime_start

        return cleaned_data
    
def validate_rut(value):
    # Remover puntos y guión si existen
    rut = value.replace(".", "").replace("-", "")
    
    if not rut[:-1].isdigit():
        raise ValidationError('RUT inválido: debe contener solo números y un dígito verificador')
    
    # Obtener dígito verificador
    dv = rut[-1].upper()
    rut = rut[:-1]
    
    # Calcular dígito verificador
    reversed_digits = map(int, reversed(str(rut)))
    factors = [2,3,4,5,6,7]
    s = sum(d * factors[i % 6] for i, d in enumerate(reversed_digits))
    expected_dv = str(11 - (s % 11))
    
    if expected_dv == '11':
        expected_dv = '0'
    elif expected_dv == '10':
        expected_dv = 'K'
    
    if dv != expected_dv:
        raise ValidationError('RUT inválido: dígito verificador incorrecto')
    
    # Formatear RUT con guión antes del dígito verificador
    formatted_rut = f"{rut}-{dv}"
    return formatted_rut
    
def format_rut(rut):
    """Format RUT with dots and dash"""
    rut = rut.replace(".", "").replace("-", "")
    dv = rut[-1]
    num = rut[:-1]
    
    # Format number with dots
    formatted = ""
    for i, digit in enumerate(reversed(num)):
        if i > 0 and i % 3 == 0:
            formatted = "." + formatted
        formatted = digit + formatted
    
    return f"{formatted}-{dv}"

class WalkInClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=False, label='Email')
    rut = forms.CharField(
        max_length=12,
        required=True,
        label='RUT',
        help_text='Formato: 12345678-9',
        validators=[validate_rut]
    )

    class Meta:
        model = Client
        fields = ['rut', 'phone', 'address']
        labels = {
            'phone': 'Teléfono',
            'address': 'Dirección'
        }

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        # Remover puntos y guión si existen
        rut = rut.replace(".", "").replace("-", "")
        
        # Validar y formatear RUT
        formatted_rut = validate_rut(rut)
        
        # Verificar si el RUT ya existe
        if Client.objects.filter(rut=formatted_rut).exists():
            raise ValidationError('Este RUT ya está registrado')
        
        return formatted_rut

    def save(self, commit=True):
        client = super().save(commit=False)
        
        # Crear usuario con nombre de usuario aleatorio si no se proporciona email
        if not self.cleaned_data.get('email'):
            import uuid
            username = f"walkin_{uuid.uuid4().hex[:8]}"
            email = f"{username}@temp.com"
        else:
            username = self.cleaned_data['email'].split('@')[0]
            email = self.cleaned_data['email']
        
        user = User.objects.create(
            username=username,
            email=email,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            is_active=True
        )
        
        client.user = user
        if commit:
            client.save()
        return client

class OnlineClientForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=200, required=True)
    rut = forms.CharField(
        max_length=12,
        required=True,
        label='RUT',
        help_text='Formato: 12345678-9',
        validators=[validate_rut]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        # Remover puntos y guión si existen
        rut = rut.replace(".", "").replace("-", "")
        
        # Validar y formatear RUT
        formatted_rut = validate_rut(rut)
        
        # Verificar si el RUT ya existe
        if Client.objects.filter(rut=formatted_rut).exists():
            raise ValidationError('Este RUT ya está registrado')
        
        return formatted_rut

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user
    
class ClientActivationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = self.client.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        
        if commit:
            user.save()
        return user
    
class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['client', 'mechanic', 'vehicle_model', 'vehicle_year', 'description', 'estimated_completion']
        widgets = {
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estimated_completion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'mechanic': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar mecánicos (solo usuarios con rol de mecánico)
        self.fields['mechanic'].queryset = UserProfile.objects.filter(role='mechanic')
        # Ordenar clientes por nombre
        self.fields['client'].queryset = Client.objects.all().order_by('user__first_name', 'user__last_name')

class WorkOrderNoteForm(forms.ModelForm):
    class Meta:
        model = WorkOrderNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    