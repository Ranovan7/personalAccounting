from django.urls import path
from . import views

urlpatterns = [
    path('category', views.category_get, name='category-get'),
    path('report', views.reports_get, name='report-get'),
    path('report_create', views.reports_create, name='report-create'),
    path('report_update', views.reports_update, name='report-update'),
    path('report_delete', views.reports_delete, name='report-delete'),
    path('statistic', views.statistic, name='statistic')
]
