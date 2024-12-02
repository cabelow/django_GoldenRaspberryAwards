from django.urls import path

from Auth.views import CustomTokenObtainPairView, CustomTokenRefreshView
from Auth.views import CustomTokenVerifyView


urlpatterns = [
    path(
        'api/token/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        CustomTokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        CustomTokenVerifyView.as_view(),
        name='token_verify'
    ),
]
