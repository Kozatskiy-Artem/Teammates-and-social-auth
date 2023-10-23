from django.urls import path

from .views import OAuthView

urlpatterns = [
    path("<str:provider>/", OAuthView.as_view(), name="oauth2"),
]
