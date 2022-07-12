from django.urls import path
from . import views

urlpatterns = [
    path('',views.stockPicker,name='stockPicker'),
    path('stocktracker/',views.stockTracker,name='stockTracker'),
]
