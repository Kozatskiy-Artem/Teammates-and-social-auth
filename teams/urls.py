from django.urls import path

from .views import ApiTeamListView, ApiTeamDetailView, ApiAddMemberView, ApiRemoveMemberView

urlpatterns = [
    path("", ApiTeamListView.as_view(), name="api-team-list"),
    path("<int:id>/", ApiTeamDetailView.as_view(), name="api-team-detail"),
    path("<int:id>/add-member", ApiAddMemberView.as_view(), name="api-add-member"),
    path("<int:id>/remove-member", ApiRemoveMemberView.as_view(), name="api-remove-member"),
]
