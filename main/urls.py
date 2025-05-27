from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('news/', views.news_list_view, name='news'),
    path('news/<slug:slug>/', views.news_detail_view, name='news_detail'),
    path('partners/', views.partners_view, name='partners'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('work/', views.work_view, name='work'),
    path('search/', views.search_view, name='search'),
]