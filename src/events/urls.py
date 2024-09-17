from django.urls import path
from . import views
#Added 
app_name = 'home'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('<int:id>/', views.eventDetailView, name='eventDetail'),
    path('<int:id>/edit/', views.eventEditView, name='eventEdit'),
    path('<int:id>/delete/', views.eventDeleteView, name='eventDelete'),
]