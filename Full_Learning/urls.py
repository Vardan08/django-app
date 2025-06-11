from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', UsersAPIList.as_view()),
    path('create/', UsersAPICreate.as_view()),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path('update/<int:pk>/', UsersAPIUpdate.as_view()),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
    path('delete/<int:pk>/', UsersAPIDelete.as_view()),
    path('details/', UserDetailsView.as_view()),
    path('details/<int:pk>/', UsersAPIDetail.as_view()),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-requests/received/', ReceivedFriendRequestsView.as_view(), name='received-friend-requests'),
    path('friend-request/accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),

]