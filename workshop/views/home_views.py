from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import *
from ..forms import *
def home(request):
    services = Product.objects.filter(category='service')[:6]
    return render(request, 'workshop/home.html', {'services': services})


@login_required
def dashboard(request):
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    context = {
        'user_profile': user_profile,
    }
    
    if request.user.is_superuser or (user_profile and user_profile.role == 'admin'):
        context.update({
            'clients': Client.objects.all(),
            'services': Product.objects.filter(category='service'),
            'work_orders': WorkOrder.objects.all()[:5],
            'reservations': Reservation.objects.filter(status='pending'),
        })
    elif user_profile and user_profile.role == 'mechanic':
        context['work_orders'] = WorkOrder.objects.filter(mechanic=user_profile)
    elif user_profile and user_profile.role == 'receptionist':
        context.update({
            'clients': Client.objects.all(),
            'work_orders': WorkOrder.objects.all()[:5],
            'reservations': Reservation.objects.filter(status='pending'),
        })
    else:
        try:
            client = Client.objects.get(user=request.user)
            context.update({
                'work_orders': WorkOrder.objects.filter(client=client),
                'reservations': Reservation.objects.filter(client=client),
            })
        except Client.DoesNotExist:
            pass
    
    return render(request, 'workshop/dashboard.html', context)

def vehicle_tracking(request):
    work_orders = []
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user)
            work_orders = WorkOrder.objects.filter(client=client).order_by('-created_at')
        except Client.DoesNotExist:
            pass
    return render(request, 'workshop/vehicle_tracking.html', {'work_orders': work_orders})