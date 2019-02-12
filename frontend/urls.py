from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('report/<int:report_id>', views.report_edit, name='report-edit'),
    path('statistics', views.statistics, name='statistics'),
    path('logout', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
]
