from django.contrib import admin
from django.urls import path, include, re_path
from .views import home
from .views import api_base
from .views import ProcessSalesReport
from .views import FrontendAppView

urlpatterns = [
    #path('', home, name='home-django'),
    path('api/', api_base, name='api'),
    path('api/process-report/', ProcessSalesReport.as_view(), name='process-report'),
    # Catch-all pattern for React
    re_path(r'^', FrontendAppView.as_view(), name='home'),
]