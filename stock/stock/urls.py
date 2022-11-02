
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/invest/', include('invest.urls')),
    path('api/account/', include('account.urls')),
    path('api/user/', include('user.urls')),
]
