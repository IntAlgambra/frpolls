from django.urls import path
from polls import views

urlpatterns = [
    path('polls_users/<int:user_id>/', views.user_answers),
    path('answer/<int:question_id>/', views.answer_question),
    path('polls/<int:pk>/questions/', views.questions),
    path('polls/<int:pk>/', views.single_poll),
    path('polls/', views.polls_list),
]
