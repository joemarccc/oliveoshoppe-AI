from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Shop URLs
    path('', views.shop_view, name='home'),  # Make shop the home page
    path('shop/', views.shop_view, name='shop'),
    path('plants/', views.plant_list, name='plant_list'),
    path('plants/create/', views.plant_create, name='plant_create'),
    path('plants/<int:plant_id>/', views.plant_detail, name='plant_detail'),
    path('plants/<int:plant_id>/edit/', views.plant_edit, name='plant_edit'),
    path('plants/<int:plant_id>/delete/', views.plant_delete, name='plant_delete'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Notification URLs
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Admin Management URLs
    path('manage/orders/', views.admin_orders, name='admin_orders'),
    path('manage/orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('manage/products/', views.admin_products, name='admin_products'),
    path('manage/products/create/', views.product_create, name='product_create'),
    path('manage/products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    
    # User Profile & Settings
    path('wishlist/', views.user_wishlist, name='wishlist'),
    path('notifications/', views.notification_settings, name='notifications'),
    path('addresses/', views.manage_addresses, name='addresses'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # Admin URLs
    path('manage/orders/pending/', views.pending_orders, name='pending_orders'),
    path('manage/categories/', views.category_management, name='category_management'),
    path('manage/inventory/', views.inventory_management, name='inventory'),
    path('manage/shipping/', views.shipping_management, name='shipping_management'),
    path('manage/refunds/', views.refund_management, name='refunds'),
    path('manage/settings/', views.store_settings, name='store_settings'),
    path('manage/settings/payment/', views.payment_settings, name='payment_settings'),
    path('manage/users/', views.user_management, name='user_management'),
    
    # API Endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/protected/', views.protected_api, name='protected_api'),
    
    # API Endpoints for Postman testing
    path('api/plants/', views.api_plants, name='api_plants'),
    path('api/plants/<int:plant_id>/', views.api_plant_detail, name='api_plant_detail'),
    path('api/cart/', views.api_cart, name='api_cart'),
    path('api/orders/', views.api_orders, name='api_orders'),
] 