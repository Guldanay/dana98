from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mamandyks/', views.MamandykListView.as_view(), name='mamandyks'),
    path('mamandyk/<int:pk>', views.MamandykDetailView.as_view(), name='mamandyk-detail'),
    path('mugalims/', views.MugalimListView.as_view(), name='mugalims'),
    path('mugalim/<int:pk>', views.MugalimDetailView.as_view(), name='mugalim-detail'),
]
urlpatterns += [
    path('mymamandyks/', views.LoanedMamandyksByUserListView.as_view(), name='my-borrowed'),
]
urlpatterns += [
    path('mamandyks/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-mamandyks-librarian'),
]