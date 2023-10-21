from django.urls import path

from .views import ApiTeamListView, ApiTeamDetailView

urlpatterns = [
    path("", ApiTeamListView.as_view(), name="api-team-list"),
    path("<int:id>/", ApiTeamDetailView.as_view(), name="api-team-detail"),
]
