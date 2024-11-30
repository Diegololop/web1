from django.urls import path
from django.contrib.auth import views as auth_views

from .views.auth_views import register
from .views.home_views import home, dashboard, vehicle_tracking
from .views.employee_views import (
    employee_list, employee_add, employee_edit, employee_delete
)
from .views.service_views import (
    service_list_public, service_list, service_add, service_edit, service_delete
)
from .views.product_views import (
    product_list_public, product_list, product_add, product_edit, product_delete
)
from .views.client_views import (
    client_list, client_add, client_edit, client_delete
)
from .views.work_order_views import (
    work_order_list, work_order_add, work_order_edit
)
from .views.reservation_views import (
    reservation_list, reservation_add, reservation_edit, reservation_confirm_delete, delete_reservation
)
from .views.public_reservation_views import (
    create_reservation, check_availability
)
from .views.inventory_views import (
    inventory_list, inventory_adjust
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='workshop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),

    path('reservations/create/', create_reservation, name='create_reservation'),
    
    # Management routes
    path('management/employees/', employee_list, name='employee_list'),
    path('management/employees/add/', employee_add, name='employee_add'),
    path('management/employees/<int:employee_id>/edit/', employee_edit, name='employee_edit'),
    path('management/employees/<int:employee_id>/delete/', employee_delete, name='employee_delete'),

    # URLs públicas de Servicios y Productos
    path('services/', service_list_public, name='service_list_public'),
    path('products/', product_list_public, name='product_list_public'),
    path('vehicle-tracking/', vehicle_tracking, name='vehicle_tracking'),
    
    # URLs de Servicios (admin)
    path('management/services/', service_list, name='service_list'),
    path('management/services/add/', service_add, name='service_add'),
    path('management/services/<int:service_id>/edit/', service_edit, name='service_edit'),
    path('management/services/<int:service_id>/delete/', service_delete, name='service_delete'),

    # URLs de Productos (admin)
    path('management/products/', product_list, name='product_list'),
    path('management/products/add/', product_add, name='product_add'),
    path('management/products/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('management/products/<int:product_id>/delete/', product_delete, name='product_delete'),
    
    # Client Management
    path('management/clients/', client_list, name='client_list'),
    path('management/clients/add/', client_add, name='client_add'),
    path('management/clients/<int:client_id>/edit/', client_edit, name='client_edit'),
    path('management/clients/<int:client_id>/delete/', client_delete, name='client_delete'),
    
    # Work Order Management
    path('management/work-orders/', work_order_list, name='work_order_list'),
    path('management/work-orders/add/', work_order_add, name='work_order_add'),
    path('management/work-orders/<int:order_id>/edit/', work_order_edit, name='work_order_edit'),

    
    path('reservations/', reservation_list, name='reservation_list'),
    path('reservations/create/', create_reservation, name='create_reservation'),
    path('reservations/delete/<int:pk>/', delete_reservation, name='delete_reservation'),
    path('reservations/check-availability/', check_availability, name='check_availability'),


    # Inventory Management
    path('management/inventory/', inventory_list, name='inventory_list'),
    path('management/inventory/<int:product_id>/adjust/', inventory_adjust, name='inventory_adjust'),
]