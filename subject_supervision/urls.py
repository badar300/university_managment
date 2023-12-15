# dissertation_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.user_login, name='login'),
    path('allstudents', views.all_students, name='all_students'),
    path('dissertations', views.all_dissertations, name='all_dissertations'),
    path('update-legal-status/<int:student_id>', views.update_legal_status, name='update_legal_status'),
    path('update-user-role/<int:student_id>', views.update_user_role, name='update-user-role'),
    path('delete-dissert/<int:theses_id>', views.delete_theses, name='delete_theses'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_theses', views.create_dissertation, name='create_dissertation'),
    path('majors', views.all_majors, name='all_majors'),
    path('update-title/<int:theses_id>', views.update_title, name='update_title'),

    path('logout/', views.user_logout, name='logout'),
    # Add more URLs for other views
]
