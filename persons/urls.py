from django.urls import path

from .views import ApiPersonListView, ApiPersonDetailView, ApiLeaveTeamView

urlpatterns = [
    path("", ApiPersonListView.as_view(), name="api-person-list"),
    path("<int:id>/", ApiPersonDetailView.as_view(), name="api-person-detail"),
    path("<int:id>/leave-team", ApiLeaveTeamView.as_view(), name="api-leave-team")
]
