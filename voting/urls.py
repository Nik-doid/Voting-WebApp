from django.urls import path
from . import views

urlpatterns = [
     path('', views.home_page, name='home_page'),
    path('vote/', views.voting_page, name='voting_page'),
    path('vote/<int:winner_id>/<int:loser_id>/', views.vote_player, name='vote_player'),

]