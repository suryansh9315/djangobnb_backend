from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConversationsListView.as_view()),
    path('start/<uuid:user_id>/', views.CreateConversationView.as_view()),
    path('<uuid:pk>/', views.ConversationsDetailsView.as_view()),
]
