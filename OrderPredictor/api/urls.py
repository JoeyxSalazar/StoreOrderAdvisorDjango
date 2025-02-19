from django.contrib import admin
from django.urls import path, include, re_path
from .views import ProcessSalesReport
from .views import FrontendAppView

urlpatterns = [
    #path('', home, name='home-django'),
    path('api/', ProcessSalesReport.as_view(), name='api'),
    # Catch-all pattern for React
    re_path(r'^', FrontendAppView.as_view(), name='home'),
]