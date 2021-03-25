from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.RoomListView.as_view(), name="index"),
    path('search/', views.SearchResultsView.as_view(), name="search"),
    path('create/', views.ChatRoomCreateView.as_view(), name="create"),
    path('update/<int:pk>/<str:name>/',
         views.ChatRoomUpdateView.as_view(), name="update"),
    path('delete/<int:pk>/<str:name>/',
         views.ChatRoomDeleteView.as_view(), name="delete"),
    path('create/private/<str:second_user>/',
         views.PrivateRoomCreateView.as_view(), name="private"),
    path('chat/<str:room_name>/', views.ChatRoomView.as_view(), name='room'),
]
