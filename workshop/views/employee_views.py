from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import *
from ..forms import *
from django.http import JsonResponse

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
@user_passes_test(is_admin)
def employee_delete(request, employee_id):
    employee = get_object_or_404(UserProfile, id=employee_id)
    if request.method == 'POST':
        user = employee.user
        user.delete()  # This will also delete the profile due to CASCADE
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('employee_list')
    return render(request, 'workshop/admin/employee_confirm_delete.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def employee_edit(request, employee_id):
    employee = get_object_or_404(UserProfile, id=employee_id)
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST, instance=employee.user)
        if form.is_valid():
            user = employee.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            employee.role = form.cleaned_data['role']
            employee.phone = form.cleaned_data['phone']
            employee.save()
            
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm(initial={
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'email': employee.user.email,
            'role': employee.role,
            'phone': employee.phone
        })
    return render(request, 'workshop/admin/employee_form.html', {
        'form': form,
        'employee': employee,
        'action': 'Editar'
    })

@login_required
@user_passes_test(is_admin)
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone']
            )
            messages.success(request, 'Empleado agregado exitosamente.')
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()
    return render(request, 'workshop/admin/employee_form.html', {
        'form': form,
        'action': 'Crear'
    })

# Employee Management Views
@login_required
@user_passes_test(is_admin)
def employee_list(request):
    employees = UserProfile.objects.exclude(role='client')
    return render(request, 'workshop/admin/employee_list.html', {'employees': employees})