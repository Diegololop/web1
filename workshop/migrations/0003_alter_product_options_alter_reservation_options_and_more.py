# Generated by Django 5.0.1 on 2024-11-25 02:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0002_add_rut_field'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['category', 'name'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={'verbose_name': 'Reserva', 'verbose_name_plural': 'Reservas'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Perfil de Usuario', 'verbose_name_plural': 'Perfiles de Usuario'},
        ),
        migrations.AlterModelOptions(
            name='workorder',
            options={'verbose_name': 'Orden de Trabajo', 'verbose_name_plural': 'Órdenes de Trabajo'},
        ),
        migrations.AlterModelOptions(
            name='workordernote',
            options={'verbose_name': 'Nota de Orden de Trabajo', 'verbose_name_plural': 'Notas de Órdenes de Trabajo'},
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('product', 'Producto'), ('service', 'Servicio')], default='product', max_length=10, verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='product',
            name='duration',
            field=models.PositiveIntegerField(blank=True, help_text='Duración estimada en minutos', null=True, verbose_name='Duración'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.client', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='description',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='service_date',
            field=models.DateTimeField(verbose_name='Fecha del Servicio'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmada'), ('cancelled', 'Cancelada')], default='pending', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.client', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='description',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='estimated_completion',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha Estimada de Término'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='mechanic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop.userprofile', verbose_name='Mecánico'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('in_progress', 'En Proceso'), ('completed', 'Completado'), ('cancelled', 'Cancelado')], default='pending', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Costo Total'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Última Actualización'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='vehicle_model',
            field=models.CharField(max_length=100, verbose_name='Modelo del Vehículo'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='vehicle_year',
            field=models.IntegerField(verbose_name='Año del Vehículo'),
        ),
        migrations.AlterField(
            model_name='workordernote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='workordernote',
            name='note',
            field=models.TextField(verbose_name='Nota'),
        ),
        migrations.AlterField(
            model_name='workordernote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='workordernote',
            name='work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.workorder', verbose_name='Orden de Trabajo'),
        ),
    ]