from django.urls import path

from .consumers import DashboardConsumer, ControlPanelConsumer

websocket_urlpatterns = [
    path('ws/<str:dashboard_slug>', DashboardConsumer.as_asgi()),
    # path('ws/kelevent/<slug:event_slug>/kata/<slug:kategori_slug>/<str:jenis_kelamin>/<int:bagan_pk>/<int:detailbagan_pk>/<int:tatami_pk>/', ControlPanelConsumer.as_asgi()),
    path('ws/kelevent/<str:event_slug>/kata/<str:kategori_slug>/<str:jenis_kelamin>/<str:bagan_pk>/<str:detailbagan_pk>/<str:tatami_pk>/', ControlPanelConsumer.as_asgi()),
] 