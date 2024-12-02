from Core.Movies.repository import MovieRepository
from Core.Winners.models import Winner


class WinnerRepository:
    @staticmethod
    def get_all_winners():
        """
        Returns all winners.
        """
        return Winner.objects.all()

    @staticmethod
    def get_winner_by_id(winner_id):
        """
        Returns a winner by ID, or None if not found.
        """
        return Winner.objects.filter(id=winner_id).first()

    @staticmethod
    def create_winner(movie, award, year):
        """
        Creates a new winner with the provided data.
        """
        return Winner.objects.create(
            movie=movie,
            award=award,
            year=year,
        )

    @staticmethod
    def update_winner(winner_id, award, year, movie_id):
        """
        Updates an existing winner with the provided data.
        """
        winner = WinnerRepository.get_winner_by_id(winner_id)
        if not winner:
            return None

        movie = MovieRepository.get_movie_by_id(movie_id)
        if not movie:
            raise ValueError("Movie could not be found.")

        winner.award = award
        winner.year = year
        winner.movie = movie
        winner.save()
        return winner

    @staticmethod
    def delete_winner(winner_id):
        """
        Deletes a winner by ID.
        """
        winner = WinnerRepository.get_winner_by_id(winner_id)
        if winner:
            winner.delete()
            return True
        return False
