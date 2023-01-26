from django.urls import path
from rudra import views

urlpatterns = [
    path('get-user/', views.User.as_view()),
    path('models/', views.AllModels.as_view()),
    path('<str:model_name>/', views.QueryModel.as_view()),
    path('query/<str:model_name>/', views.DeepQueryModel.as_view())
]
