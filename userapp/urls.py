from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import featured_product
urlpatterns = [
    path('', featured_product, name='product_details'),
    path('', featured_product, name='loginview'),
    path('',views.loginview,name='loginview'),
    path('register/loginview',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('loginview/', views.logview, name='loginview'),
     path('forgot', auth_views.PasswordResetView.as_view(), name='password_reset'),
     path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),  
    path('customer_list/', views.customer_list, name='customer_list'),
    path('change_status/<int:user_id>/', views.change_status, name='change_status'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('change_staff_status/<int:staff_id>/', views.change_staff_status, name='change_staff_status'),
    path('contact/', views.contact, name='contact'),
    path('adminprofile/', views.adminprofile, name='adminprofile'),
    path('viewproduct/', views.view_product, name='viewproduct'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('products/', views.product_grid, name='products'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('cutomerprofile/', views.profile, name='customerprofile'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('view_cart/<int:product_id>/', views.view_cart, name='view_cart'),
     path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('add_product/', views.add_product, name='add_product'),
     path('category/', views.category_view, name='category'),
    path('payment/', views.rentnxt, name='payment'), 
    
    path('feedback/',views.feedback_view, name='feedback_form'),
    path('orderlist/', views.orderlist, name='orderlist'),
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)