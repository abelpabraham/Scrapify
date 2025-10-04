from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('',views.index, name="index"),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name="contact"),
    path('register_admin/',views.register_admin, name="register_admin"),
    path('pickup-map/', views.pickup_map, name='pickup_map'),

    
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    
    # Admin
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("category/add/", views.add_category, name="add_category"),
    path("category/list/", views.list_categories, name="list_categories"),
    path("category/edit/<int:category_id>/", views.edit_category, name="edit_category"),
    path("category/delete/<int:category_id>/", views.delete_category, name="delete_category"),
    path("dealers/", views.dealers_list, name="dealers_list"),
    path("admin/toggle/<int:user_id>/active", views.toggle_user_active, name="toggle_user_active"),
    path("dealers/<int:dealer_id>/rates/", views.dealer_rates, name="dealer_rates"),
    path("approve-rate/<int:rate_id>/", views.approve_rate, name="approve_rate"),
    path("reject-rate/<int:rate_id>/", views.reject_rate, name="reject_rate"),
    path("admin/sellers/", views.sellers_list, name="sellers_list"),

    
    #seller
    path("dashboard/seller/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/profile/", views.profile_view, name="seller_profile"),
    path("seller/create_pickup_request/", views.create_pickup_request, name="create_pickup_request"),
    path("seller/my-requests/", views.my_pickup_requests, name="my_pickup_requests"),
    path("seller/request/<int:request_id>/cancel/", views.cancel_pickup_request, name="cancel_pickup_request"),
    path("seller/request/<int:request_id>/edit/", views.edit_pickup_request, name="edit_pickup_request"),
    path("seller/request/<int:request_id>/reschedule/", views.request_reschedule, name="request_reschedule"),

   
    # Dealer
    path("dashboard/dealer/", views.dealer_dashboard, name="dealer_dashboard"),
    path("dealer/profile/", views.profile_view, name="dealer_profile"),
    path("dealer/rates/", views.manage_rates, name="manage_rates"),   
    path("dealer/pickup_requests", views.dealer_pickup_requests, name="dealer_pickup_requests"),  
    path("dealer/pickup/<int:request_id>/accept/", views.accept_pickup_request, name="accept_pickup_request"),
    path("dealer/accepted_pickup_requests/", views.dealer_accepted_pickup_requests, name="dealer_accepted_pickup_requests"),
    path("dealer/pickup/<int:request_id>/verify/", views.verify_pickup_request, name="verify_pickup_request"), 
    path("dealer/pickup/<int:request_id>/schedule/", views.schedule_pickup, name="schedule_pickup"),
    path("dealer/reschedules/", views.dealer_reschedule_list, name="dealer_reschedule_list"),
    path("dealer/reschedule/<int:rr_id>/<str:action>/", views.respond_reschedule, name="respond_reschedule"),

    
    
    
    
    
]