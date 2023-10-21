from django.urls import path

from .views import ApiPersonListView, ApiPersonDetailView

urlpatterns = [
    path("", ApiPersonListView.as_view(), name="api-person-list"),
    path("<int:id>/", ApiPersonDetailView.as_view(), name="api-person-detail"),
]
