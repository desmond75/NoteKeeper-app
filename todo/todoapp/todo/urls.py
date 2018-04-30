from . import views
from django.urls import path
from django.contrib import admin
#from django.contrib.auth import views as auth_views

admin.site.site_header = 'Notebook'
app_name = 'todo'

urlpatterns = [
     path('', views.home, name='home' ),
     #path('login/', views.login, name='login'),
     path('signup/', views.signup, name='signup'),
     path('dashboard/',views.dashboard, name='dashboard'),
     path('<int:id>/create_note/', views.create_note, name='create_note'),
     path('<int:id>/view_note', views.view_note, name='view_note'), 
     path('<int:id>/edit', views.edit, name='edit'),
     path('<int:id>/delete', views.delete_note, name='delete'),
     path('<int:id>change_password',views.change_password, name='change_password')

]