from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='index'),
    path('register/', views.RegisterView, name='register'),
    path('terms_of_service/', views.TermView, name='term'),
    path('privacy_policy/', views.PrivacyView, name='privacy'),
    path('about/', views.AboutView, name='about'),
    path('contact/', views.ContactView, name='contact'),
    path('<int:pk>/', views.DetailView, name='detail'),
    path('review/<int:pk>/', views.AddReviewView, name='addreview'),
    path('add_cart/<name>/', views.AddOrderView, name='addorder'),
    path('order/<int:pk>/', views.DetailOrderView, name='detailorder'),
    path('query/<int:pk>/', views.QueryView, name='addquery'),
    path('view_cart/', views.OrderView, name='orders'),
    path('like/<int:pk>/', views.LikeView, name='like'),
    path('<category>/', views.CategoryView, name='category'),
]
