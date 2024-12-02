from django.urls import path

from Core.Movies.view import ImportMovieCSVView, MoviesView, ProducersWithWinnerView, StudiosWithWinnersView, YearWithWinnerView, YearsWithMultipleWinnersView
from Core.Producers.view import ProducerView
from Core.Studio.view import StudioView


urlpatterns = [
    path('producers/', ProducerView.as_view(), name='producer-list'),
    path('producers/<int:producer_id>/', ProducerView.as_view(), name='producer-detail'),
    path('studios/', StudioView.as_view(), name='studio-list'),
    path('studios/<int:studio_id>/', StudioView.as_view(), name='studio-detail'),
    path('movies/', MoviesView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/', MoviesView.as_view(), name='movie-detail'),
    path('movies/import/csv/', ImportMovieCSVView.as_view(), name='winner-import-csv'),
    path('movies/years/multiple-winners/', YearsWithMultipleWinnersView.as_view(), name='years-multiple-winners'),
    path('movies/studios-winners/', StudiosWithWinnersView.as_view(), name='studios-with-winners'),
    path('movies/producers-winners/', ProducersWithWinnerView.as_view(), name='producers-with-winner'),
    path('movies/year-with-winners/', YearWithWinnerView.as_view(), name='year-with-winner'),
]
