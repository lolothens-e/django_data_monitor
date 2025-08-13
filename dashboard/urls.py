from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path("base/", views.index, name="index"),
   path("", views.index, name="index"),
   path('login/', auth_views.LoginView.as_view(template_name='security/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]