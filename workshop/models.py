from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('client', 'Cliente'),
        ('mechanic', 'Mecánico'),
        ('receptionist', 'Recepcionista'),
        ('admin', 'Administrador'),
    ])
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    phone = models.CharField(max_length=15, verbose_name='Teléfono')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.rut}"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('product', 'Producto'),
        ('service', 'Servicio'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.IntegerField(verbose_name='Stock')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Imagen')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='product', verbose_name='Categoría')
    duration = models.PositiveIntegerField(help_text='Duración estimada en minutos', null=True, blank=True, verbose_name='Duración')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Proceso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    mechanic = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mecánico')
    vehicle_model = models.CharField(max_length=100, verbose_name='Modelo del Vehículo')
    vehicle_year = models.IntegerField(verbose_name='Año del Vehículo')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    estimated_completion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Estimada de Término')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Costo Total')

    def __str__(self):
        return f"OT #{self.id} - {self.client}"

    class Meta:
        verbose_name = 'Orden de Trabajo'
        verbose_name_plural = 'Órdenes de Trabajo'

class WorkOrderNote(models.Model):
    work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancel_reason = models.BooleanField(default=False)  # Nuevo campo

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Nota para orden #{self.work_order.id} - {self.created_at}'

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    services = models.ManyToManyField(Product, verbose_name='Servicios')
    service_date = models.DateTimeField(verbose_name='Fecha del Servicio')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    total_duration = models.PositiveIntegerField(help_text='Duración total en minutos', verbose_name='Duración Total')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Total')

    def __str__(self):
        return f"Reserva de {self.client} para {self.service_date}"

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('add', 'Entrada'),
        ('remove', 'Salida'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES, verbose_name='Tipo de Movimiento')
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')
    reason = models.TextField(verbose_name='Motivo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} de {self.product.name} - {self.quantity} unidades"
    
