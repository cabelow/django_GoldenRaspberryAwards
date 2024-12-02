from io import StringIO
from django.core.paginator import Paginator
from xml.dom import ValidationErr
import pandas as pd
from django.db.models import QuerySet
from Core.Movies.models import Movie
from Core.Movies.repository import MovieRepository
from Core.Movies.serializer import MovieSerializer
from Core.Producers.models import Producer
from Core.Producers.repository import ProducerRepository
from Core.Studio.repository import StudioRepository
from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)


class MovieService:
    @staticmethod
    def get_all_movies(filters=None, page=1, size=10):
        try:
            page = int(filters.get("page", 1))
            size = int(filters.get("size", 10))
            if filters is None:
                filters = {}

            if "winner" in filters:
                winner = filters["winner"].lower()
                if winner in ["true", "1"]:
                    filters["winner"] = True
                elif winner in ["false", "0"]:
                    filters["winner"] = False
                else:
                    raise ValueError("Invalid value for 'winner'. Expected 'true', 'false'")

            if "year" in filters:
                try:
                    filters["year"] = int(filters["year"])
                except ValueError:
                    raise ValueError("Invalid value for 'year'. Expected an integer.")

            movies = MovieRepository.get_all_movies(filters)
            paginator = Paginator(movies, size)
            paginated_movies = paginator.get_page(page)
            serialized_movies = MovieSerializer(
                paginated_movies.object_list,
                many=True,
                context={'request': None}
            ).data

            my_return = {
                "content": serialized_movies,
                "pageable": {
                    "sort": {
                        "sorted": False,
                        "unsorted": True
                    },
                    "pageSize": size,
                    "pageNumber": page - 1,
                    "offset": (page - 1) * size,
                    "paged": True,
                    "unpaged": False
                },
                "totalElements": paginator.count,
                "last": not paginated_movies.has_next(),
                "totalPages": paginator.num_pages,
                "first": paginated_movies.number == 0,
                "sort": {
                    "sorted": False,
                    "unsorted": True
                },
                "number": paginated_movies.number,
                "numberOfElements": len(paginated_movies),
                "size": size
            }
            return my_return
        except ValueError as ve:
            logger.warning(f"Invalid filter value: {ve}")
            raise
        except KeyError as ke:
            logger.error(f"Key error: {ke}")
            raise
        except Exception as e:
            logger.error(f"Error getting all movies: {e}")
            raise


    @staticmethod
    def get_movie_by_id(movie_id):
        try:
            movie = MovieRepository.get_movie_by_id(movie_id)
            if not movie:
                logger.warning(f"Movie with ID {movie_id} not found.")
                return None
            return movie
        except Exception as e:
            logger.error(f"Error getting movie by ID {movie_id}: {e}")
            raise

    @staticmethod
    def create_movie(title, year, producer_data, studio_data, winner=False):
        try:
            producers = [
                ProducerRepository.get_or_create_producer([producer_name.strip()])[0]
                for producer_name in producer_data
            ]
            studios = [
                StudioRepository.get_or_create_studio({'name': studio_name.strip()})
                for studio_name in studio_data
            ]
            movie, created = Movie.objects.get_or_create(
                title=title,
                year=year,
                defaults={'winner': winner}
            )
            if created:
                movie.producer.add(*producers)
                movie.studio.add(*studios)

            return movie
        except Exception as e:
            logger.error(f"Error creating movie '{title}': {e}")
            raise

    @staticmethod
    def update_movie(movie_id, title, year, producer_data, studio_data, winner=None):
        try:
            movie = MovieRepository.update_movie(movie_id, title, year, producer_data, studio_data, winner)
            if movie:
                logger.info(f"Movie ID {movie_id} updated successfully.")
                return movie
            else:
                logger.warning(f"Movie ID {movie_id} not found for update.")
                return None
        except Exception as e:
            logger.error(f"Error updating movie ID {movie_id}: {e}")
            raise

    @staticmethod
    def delete_movie(movie_id):
        try:
            success = MovieRepository.delete_movie(movie_id)
            if success:
                logger.info(f"Movie ID {movie_id} deleted successfully.")
            else:
                logger.warning(f"Movie ID {movie_id} not found for deletion.")
            return success
        except Exception as e:
            logger.error(f"Error deleting movie ID {movie_id}: {e}")
            raise

    @staticmethod
    def get_years_with_multiple_winners():
        try:
            years_with_multiple_winners = MovieRepository.get_years_with_multiple_winners()
            return years_with_multiple_winners
        except Exception as e:
            logger.error(f"Error fetching years with multiple winners: {e}")
            raise

    @staticmethod
    def get_studios_with_winners():
        try:
            studios_with_wins = MovieRepository.get_studios_with_winners()
            formatted_studios = [
                {
                    "name": studio["studio__name"],
                    "winCount": studio["wins"]
                }
                for studio in studios_with_wins
            ]
            return {"studios": formatted_studios}
        except Exception as e:
            logger.error(f"Error fetching studios with most wins: {e}")
            raise

    @staticmethod
    def get_producers_with_winner_intervals():
        try:
            producers_with_intervals = MovieRepository.get_producers_with_winner_intervals()
            return producers_with_intervals
        except Exception as e:
            logger.error(f"Error fetching producers with winner intervals: {e}")
            raise

    @staticmethod
    def get_movies_with_winner(filters=None):
        try:
            if filters is None:
                filters = {}
            if "winner" in filters:
                winner = filters["winner"].lower()
                if winner in ["true", "1"]:
                    filters["winner"] = True
                elif winner in ["false", "0"]:
                    filters["winner"] = False
                else:
                    raise ValueError("Invalid value for 'winner'. Expected 'true', 'false'")
            if "year" in filters:
                try:
                    filters["year"] = int(filters["year"])
                except ValueError:
                    raise ValueError("Invalid value for 'year'. Expected an integer.")
            movies = MovieRepository.get_all_movies(filters)
            serialized_movies = MovieSerializer(
                movies,
                many=True,
                context={'request': None}
            ).data
            return serialized_movies
        except ValueError as ve:
            logger.warning(f"Invalid filter value: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error getting movies with filters {filters}: {e}")
            raise




class ImportMovieCSVService:
    REQUIRED_COLUMNS = {"year", "title", "studios", "producers", "winner"}

    @staticmethod
    def process_file(file):
        ImportMovieCSVService.validate_file_type(file)
        try:
            file_content = file.read().decode("utf-8")
            data = pd.read_csv(StringIO(file_content), delimiter=";", engine="python")
        except Exception as e:
            raise serializers.ValidationError(f"Error reading the file: {e}")
        ImportMovieCSVService.validate_file_header(data)
        return ImportMovieCSVService.process_data(data)

    @staticmethod
    def validate_file_type(file):
        valid_extensions = [".csv", ".xls", ".xlsx"]
        if not any(file.name.endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError("Unsupported file type. Please upload a CSV or Excel file.")

    @staticmethod
    def validate_file_header(dataframe):
        missing_columns = ImportMovieCSVService.REQUIRED_COLUMNS - set(dataframe.columns)
        if missing_columns:
            raise serializers.ValidationError(f"Invalid file header. Missing columns: {', '.join(missing_columns)}")

    @staticmethod
    def normalize_winner(value):
        """Normalize winner column to a boolean value."""
        if pd.isna(value):
            return False
        if isinstance(value, str):
            value = value.strip().lower()
            if value in {"yes", "y", "1", "sim"}:
                return True
        elif isinstance(value, (int, float)) and value == 1:
            return True

        return False

    @staticmethod
    def process_data(dataframe):
        accepted = []
        errors = []
        try:
            dataframe["winner"] = dataframe["winner"].apply(ImportMovieCSVService.normalize_winner)
        except Exception as e:
            raise serializers.ValidationError(f"Error processing 'winner' column: {e}")

        for _, row in dataframe.iterrows():
            try:
                title = row["title"].strip()
                year = int(row["year"])
                studios = [name.strip() for name in row["studios"].split(",")]
                producers = [name.strip() for name in row["producers"].split(",")]
                winner = row["winner"]
                movie = MovieService.create_movie(title, year, producers, studios, winner)
                accepted.append({
                    "title": title,
                    "year": year,
                    "producers": producers,
                    "studios": studios,
                    "winner": winner
                })
            except Exception as e:
                errors.append({
                    "title": row.get("title", "Unknown"),
                    "error": str(e)
                })

        return {"accepted": accepted, "errors": errors}

