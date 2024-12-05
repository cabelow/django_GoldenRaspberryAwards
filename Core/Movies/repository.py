from Core.Movies.models import Movie
from Core.Producers.repository import ProducerRepository
from Core.Studio.repository import StudioRepository
from django.db.models import Count
from django.db.models import Count, Min, Max, Q
import logging
logger = logging.getLogger(__name__)


class MovieRepository:
    @staticmethod
    def get_all_movies(filters=None):
        try:
            movies = Movie.objects.all()
            if filters:
                if "winner" in filters:
                    if isinstance(filters["winner"], bool):
                        movies = movies.filter(winner=filters["winner"])
                    else:
                        raise ValueError("Invalid value for 'winner'. Accepts True or False only.")
                if "year" in filters:
                    if isinstance(filters["year"], int):
                        movies = movies.filter(year=filters["year"])
                    else:
                        raise ValueError("Invalid value for 'year'. Expected an integer.")
            return  movies.order_by('id')
        except Exception as e:
            logger.error(f"Error getting movies with filters {filters}: {e}")
            raise




    @staticmethod
    def get_movie_by_id(movie_id):
        try:
            return Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_movie(title, year, producer_data, studio_data, winner=False):
        producers = ProducerRepository.get_or_create_producer(producer_data)
        studio = StudioRepository.get_or_create_studio(studio_data)
        movie, created = Movie.objects.get_or_create(
            title=title,
            year=year,
            studio=studio,
            defaults={'winner': winner}
        )
        if created:
            movie.producers.add(*producers)
        return movie

    @staticmethod
    def create_movie(title, year, producer, studio, winner=False):
        return Movie.objects.create(
            title=title,
            year=year,
            producer=producer,
            studio=studio,
            winner=winner
        )

    @staticmethod
    def update_movie(movie_id, title, year, producer_data, studio_data, winner=None):
        movie = MovieRepository.get_movie_by_id(movie_id)
        if movie:
            producer = ProducerRepository.get_or_create_producer(producer_data)
            studio = StudioRepository.get_or_create_studio(studio_data)
            movie.title = title
            movie.year = year
            movie.producer = producer
            movie.studio = studio
            if winner is not None:
                movie.winner = winner
            movie.save()
            return movie
        return None

    @staticmethod
    def delete_movie(movie_id):
        movie = MovieRepository.get_movie_by_id(movie_id)
        if movie:
            movie.delete()
            return True
        return False

    @staticmethod
    def get_years_with_multiple_winners():
        try:
            year_counts = (
                Movie.objects.filter(winner=True)
                .values('year')
                .annotate(count=Count('year'))
                .filter(count__gt=1)
            )
            years_with_multiple_winners = [
                {'year': entry['year'], 'winnerCount': entry['count']}
                for entry in year_counts
            ]
            return years_with_multiple_winners
        except Exception as e:
            logger.error(f"Error fetching years with multiple winners from the repository: {e}")
            raise

    @staticmethod
    def get_studios_with_winners():
        try:
            studios_with_wins = (
                Movie.objects.filter(winner=True)
                .values('studio__name')
                .annotate(wins=Count('studio'))
                .order_by('-wins')
            )
            return studios_with_wins
        except Exception as e:
            logger.error(f"Error fetching studios with most wins from the repository: {e}")
            raise

    @staticmethod
    def get_producers_with_winner_intervals():
        try:
            producers_with_intervals = (
                Movie.objects.filter(winner=True)
                .values('producer__name')
                .annotate(
                    min_year=Min('year'),
                    max_year=Max('year'),
                    count=Count('id')
                )
                .filter(count__gte=2)
                .order_by('-max_year', 'min_year')
            )
            producers_with_intervals_list = []
            for entry in producers_with_intervals:
                entry['interval'] = entry['max_year'] - entry['min_year']
                producers_with_intervals_list.append(entry)
            if producers_with_intervals_list:
                min_entry = min(producers_with_intervals_list, key=lambda x: x['interval'])
                max_entry = max(producers_with_intervals_list, key=lambda x: x['interval'])
                response = {
                    "min": [{
                        "producer": min_entry['producer__name'],
                        "interval": min_entry['interval'],
                        "previousWin": min_entry['min_year'],
                        "followingWin": min_entry['max_year']
                    }],
                    "max": [{
                        "producer": max_entry['producer__name'],
                        "interval": max_entry['interval'],
                        "previousWin": max_entry['min_year'],
                        "followingWin": max_entry['max_year']
                    }]
                }
                return response
            return {}
        except Exception as e:
            logger.error(f"Error fetching producers with winner intervals: {e}")
            raise
