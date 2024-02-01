from django.urls import path
from . import views
from .views import PostDeleteView
urlpatterns = [
    path('', views.home,name='index'),
    path('delete/<int:pk>',  PostDeleteView.as_view() ,name='link-delete'),
]
