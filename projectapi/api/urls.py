from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('profile-list/', views.profileList, name="profile-list"),
    path('profile-create/', views.createProfile, name="profile-create"),
    path('get-user-agreement/', views.getUserAgreement, name='generate_pdf'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('team-create/', views.createTeam, name='create-team'),
    path('teams-list/', views.teamDetailView.as_view(), name="teams-list"),
]