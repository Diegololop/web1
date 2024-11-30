from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
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

@login_required
@user_passes_test(is_admin_or_receptionist)
def work_order_list(request):
    search_query = request.GET.get('search', '')
    work_orders = WorkOrder.objects.all()

    if search_query:
        work_orders = work_orders.filter(
            Q(id__icontains=search_query) |
            Q(client__user__first_name__icontains=search_query) |
            Q(client__user__last_name__icontains=search_query) |
            Q(client__rut__icontains=search_query) |
            Q(vehicle_model__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    work_orders = work_orders.order_by('-created_at')
    
    return render(request, 'workshop/admin/work_order_list.html', {
        'work_orders': work_orders,
        'search_query': search_query
    })

@login_required
@user_passes_test(is_admin_or_receptionist)
def work_order_add(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            work_order = form.save(commit=False)
            work_order.status = 'pending'
            work_order.save()

            # Crear nota inicial si se proporcionó
            initial_note = request.POST.get('initial_note')
            if initial_note:
                WorkOrderNote.objects.create(
                    work_order=work_order,
                    user=request.user,
                    note=initial_note
                )

            messages.success(request, 'Orden de trabajo creada exitosamente.')
            return redirect('work_order_list')
    else:
        form = WorkOrderForm()
    
    return render(request, 'workshop/admin/work_order_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
def work_order_edit(request, order_id):
    work_order = get_object_or_404(WorkOrder, id=order_id)
    is_mechanic = hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'mechanic'
    
    # Obtener la nota de cancelación si existe
    cancel_note = None
    if work_order.status == 'cancelled':
        cancel_note = WorkOrderNote.objects.filter(
            work_order=work_order,
            is_cancel_reason=True
        ).last()

    if request.method == 'POST':
        if 'change_status' in request.POST:
            new_status = request.POST.get('change_status')
            note_text = request.POST.get('note', '')
            
            # Si el estado es "cancelled", usar el motivo proporcionado
            if new_status == 'cancelled':
                # Primero actualizamos el estado
                work_order.status = new_status
                work_order.save()
                
                # Crear nota con el motivo de cancelación
                cancel_note = WorkOrderNote.objects.create(
                    work_order=work_order,
                    user=request.user,
                    note=note_text,
                    is_cancel_reason=True
                )
                
                messages.success(request, 'Orden cancelada correctamente.')
            else:
                # Actualizar estado
                work_order.status = new_status
                work_order.save()
                
                # Crear nota para otros cambios de estado
                WorkOrderNote.objects.create(
                    work_order=work_order,
                    user=request.user,
                    note=f'Estado cambiado a {work_order.get_status_display()}',
                    is_cancel_reason=False
                )
                
                messages.success(request, 'Estado actualizado correctamente.')
            
            return redirect('work_order_edit', order_id=work_order.id)
        
        # Procesar el formulario principal si no es un cambio de estado
        form = WorkOrderForm(request.POST, instance=work_order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orden de trabajo actualizada correctamente.')
            return redirect('work_order_list')
    else:
        form = WorkOrderForm(instance=work_order)
    
    context = {
        'work_order': work_order,
        'is_mechanic': is_mechanic,
        'status_choices': WorkOrder.STATUS_CHOICES,
        'notes': WorkOrderNote.objects.filter(work_order=work_order).order_by('-created_at'),
        'cancel_note': cancel_note,
        'form': form,
        'note_form': WorkOrderNoteForm() if not is_mechanic else None,
        'action': 'Editar'
    }
    
    return render(request, 'workshop/admin/work_order_form.html', context)