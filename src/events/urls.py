from django.urls import path
from . import views
from .views import CreateCheckoutSession
# from views import CreateCheckoutSessionsView
#Added 
app_name = 'home'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('<int:id>/', views.eventDetailView, name='eventDetail'),
    path('<int:id>/edit/', views.eventEditView, name='eventEdit'),
    path('<int:id>/delete/', views.eventDeleteView, name='eventDelete'),
    path('create-checkout-session/', CreateCheckoutSession, name='createCheckoutSession'),
    # path('create-checkout-session/', views.CreateCheckoutSessionsView.as_view(), name='CreateCheckoutSession'),
    # path('product-landing-page/', ProductLandingPageView.as_view(), name='prroductionLandingPage')
    # path('charge/', views.charge, name="charge"),
    # path('success/<str:args>/', views.successMsg, name="success"),
]

# url patterns for events"