from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from invest import views


router = DefaultRouter()
router.register('invests', views.InvestViewSet)

app_name = 'invest'

urlpatterns = [
    path('', include(router.urls))
]
