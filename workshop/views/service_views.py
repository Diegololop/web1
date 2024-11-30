from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from ..models import *
from ..forms import *

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role == 'admin')

def is_admin_or_receptionist(user):
    if user.is_superuser:
        return True
    if hasattr(user, 'userprofile'):
        return user.userprofile.role in ['admin', 'receptionist']
    return False

def can_view_work_order(user, work_order):
    if user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role in ['admin', 'receptionist']):
        return True
    if hasattr(user, 'userprofile') and user.userprofile.role == 'mechanic':
        return work_order.mechanic == user.userprofile
    return False

def can_manage_inventory(user):
    return user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role in ['admin', 'mechanic'])
def service_list_public(request):
    services = Product.objects.filter(category='service')
    return render(request, 'workshop/service_list_public.html', {'services': services})


@login_required
@user_passes_test(is_admin)
def service_list(request):
    services = Product.objects.filter(category='service')
    return render(request, 'workshop/admin/service_list.html', {'services': services})

@login_required
@user_passes_test(is_admin)
def service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.category = 'service'
            service.save()
            messages.success(request, 'Servicio creado exitosamente.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'workshop/admin/service_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
@user_passes_test(is_admin)
def service_edit(request, service_id):
    service = get_object_or_404(Product, id=service_id, category='service')
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio actualizado exitosamente.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'workshop/admin/service_form.html', {
        'form': form,
        'service': service,
        'action': 'Editar'
    })

@login_required
@user_passes_test(is_admin)
def service_delete(request, service_id):
    service = get_object_or_404(Product, id=service_id, category='service')
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect('service_list')
    return render(request, 'workshop/admin/service_confirm_delete.html', {'service': service})