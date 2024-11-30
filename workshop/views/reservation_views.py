from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Client, Product, Reservation
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from ..models import Reservation, Service
from ..forms import ReservationForm


def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Si el usuario está autenticado, asigna automáticamente sus datos
            if request.user.is_authenticated:
                reservation.user = request.user
            reservation.save()
            return redirect('reservation_success')  # Redirige a una página de éxito
    else:
        form = ReservationForm()
    
    context = {'form': form}
    return render(request, 'reservation_form.html', context)

@login_required
def reservation_list(request):
    search_date = request.GET.get('date')
    reservations = Reservation.objects.all().order_by('-service_date')
    
    if search_date:
        try:
            date = datetime.strptime(search_date, '%Y-%m-%d').date()
            reservations = reservations.filter(service_date__date=date)
        except ValueError:
            messages.error(request, 'Formato de fecha inválido')
    
    context = {
        'reservations': reservations,
        'search_date': search_date
    }
    return render(request, 'workshop/admin/reservation_list.html', context)

@require_POST
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.delete()
    messages.success(request, 'Reserva eliminada exitosamente.')
    return redirect('reservation_list')

def check_availability(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'Fecha requerida'}, status=400)
    
    working_hours = [f"{hour:02d}:00" for hour in range(9, 19)]
    
    existing_reservations = Reservation.objects.filter(date__date=date)
    booked_times = [r.date.strftime('%H:%M') for r in existing_reservations]
    
    available_hours = []
    for time in working_hours:
        available = time not in booked_times
        slot = {
            'time': time,
            'available': available,
            'reason': 'Horario no disponible' if not available else None
        }
        available_hours.append(slot)
    
    return JsonResponse({
        'all_hours': available_hours
    })



@login_required
def reservation_add(request):
    if request.method == 'POST':
        try:
            client_id = request.POST.get('client')
            service_ids = request.POST.getlist('services')
            date = request.POST.get('date')
            time = request.POST.get('time')
            description = request.POST.get('description', '')

            if not all([client_id, service_ids, date, time]):
                messages.error(request, 'Todos los campos son requeridos.')
                return redirect('reservation_add')

            client = get_object_or_404(Client, id=client_id)
            services = Product.objects.filter(id__in=service_ids, category='service')

            if not services.exists():
                messages.error(request, 'Debe seleccionar al menos un servicio.')
                return redirect('reservation_add')

            service_date = timezone.make_aware(
                datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            )

            total_duration = sum(service.duration or 0 for service in services)
            total_price = sum(service.price for service in services)

            reservation = Reservation.objects.create(
                client=client,
                service_date=service_date,
                description=description,
                total_duration=total_duration,
                total_price=total_price,
                status='pending'
            )
            reservation.services.set(services)

            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('reservation_list')

        except Exception as e:
            messages.error(request, f'Error al crear la reserva: {str(e)}')
            return redirect('reservation_add')

    context = {
        'clients': Client.objects.all(),
        'services': Product.objects.filter(category='service'),
        'action': 'Crear'
    }
    return render(request, 'workshop/admin/reservation_form.html', context)

@login_required
def reservation_edit(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        try:
            client_id = request.POST.get('client')
            service_ids = request.POST.getlist('services')
            date = request.POST.get('date')
            time = request.POST.get('time')
            description = request.POST.get('description', '')

            if not all([client_id, service_ids, date, time]):
                messages.error(request, 'Todos los campos son requeridos.')
                return redirect('reservation_edit', reservation_id=reservation_id)

            client = get_object_or_404(Client, id=client_id)
            services = Product.objects.filter(id__in=service_ids, category='service')
            
            if not services.exists():
                messages.error(request, 'Debe seleccionar al menos un servicio.')
                return redirect('reservation_edit', reservation_id=reservation_id)

            service_date = timezone.make_aware(
                datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            )

            reservation.client = client
            reservation.service_date = service_date
            reservation.description = description
            reservation.total_duration = sum(service.duration or 0 for service in services)
            reservation.total_price = sum(service.price for service in services)
            reservation.save()
            
            reservation.services.set(services)

            messages.success(request, 'Reserva actualizada exitosamente.')
            return redirect('reservation_list')

        except Exception as e:
            messages.error(request, f'Error al actualizar la reserva: {str(e)}')
            return redirect('reservation_edit', reservation_id=reservation_id)

    context = {
        'reservation': reservation,
        'clients': Client.objects.all(),
        'services': Product.objects.filter(category='service'),
        'action': 'Editar'
    }
    return render(request, 'workshop/admin/reservation_form.html', context)

@login_required
def reservation_confirm_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason')
        if cancel_reason:
            reservation.status = 'cancelled'
            reservation.save()
            messages.success(request, 'Reserva cancelada exitosamente.')
        else:
            messages.error(request, 'Debe proporcionar un motivo para la cancelación.')
    
    return redirect('reservation_list')