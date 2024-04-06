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
    path('add_product/', views.add_product, name='add_product'),
    path('category/', views.category_view, name='category'),
    path('orderlist/', views.order_list, name='order_list'), 
    path('submit-feedback/', views.feedback_submit, name='feedback_submit'),
    path('feedbacks/', views.feedback_list, name='feedback_list'),
    path('calculate_purity', views.golditem_list, name='calculate_purity'),
    path('golditem/<int:gold_item_id>/download-pdf/', views.generate_pdf, name='generate_pdf'),     
    path('delete_product/<int:product_id>/',views. delete_product, name='delete_product'),
    path('product_details/<int:gold_item_id>/product_pdf/', views.product_pdf, name='product_pdf'),
    path('product_data_endpoint/', views.product_data_endpoint_view, name='product_data_endpoint'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('orderdetails/', views.orderdetails, name='orderdetails'),
    path('manage/', views.manage, name='manage'), 
    path('payment_success/', views.payment_success, name='payment_success'),
    path('generate-pdf-bill/<int:payment_id>/', views.generate_pdf_bill, name='generate_pdf_bill'),
    

 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)