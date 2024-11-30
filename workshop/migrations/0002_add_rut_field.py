from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='rut',
            field=models.CharField(
                max_length=12,
                unique=True,
                verbose_name='RUT',
                default='00.000.000-0'  # Temporary default value
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='total_duration',
            field=models.PositiveIntegerField(
                help_text='Duración total en minutos',
                verbose_name='Duración Total',
                default=0
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(
                max_digits=10,
                decimal_places=2,
                verbose_name='Precio Total',
                default=0
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='services',
            field=models.ManyToManyField(
                to='workshop.product',
                verbose_name='Servicios'
            ),
        ),
    ]