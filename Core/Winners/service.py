from Core.Movies.service import MovieService
from Core.Winners.repository import WinnerRepository


class WinnerService:
    @staticmethod
    def get_all_winners():
        return WinnerRepository.get_all_winners()

    @staticmethod
    def get_winner_by_id(winner_id):
        return WinnerRepository.get_winner_by_id(winner_id)

    @staticmethod
    def create_winner(title, year, producer_data, studio_data, movie_title):
        movie = MovieService.get_or_create_movie(
            movie_title,
            producer_data,
            studio_data
        )
        if movie:
            winner = WinnerRepository.create_winner(movie, title, year)
            return winner
        return None

    @staticmethod
    def update_winner(winner_id, movie_id, award, year):
        movie = MovieService.get_movie_by_id(movie_id)
        if not movie:
            return None
        return WinnerRepository.update_winner(
            winner_id,
            movie,
            award,
            year
        )

    @staticmethod
    def delete_winner(winner_id):
        return WinnerRepository.delete_winner(winner_id)


class WinnerCSVService:
    def __init__(self, file):
        if not hasattr(file, 'read'):
            raise ValueError("The file must be an InMemoryUploadedFile")
        self.file = file

    def process_and_prepare_data(self, content, old_delim=', ', new_delim=';'):
        modified_content = content.replace(old_delim, new_delim)
        data_list = []
        data_list_error = []

        for idx, line in enumerate(modified_content.splitlines()):
            if idx == 0:
                continue
            values = line.split(new_delim)
            if len(values) > 3:
                for i in range(4, len(values)):
                    if values[i]:
                        winner = WinnerService.create_winner(
                            title=values[i],
                            year=int(values[0]),
                            producer_data=values[3],
                            studio_data=values[2],
                            movie_title=values[1]
                        )
                        if winner:
                            data_list.append(winner)
                        else:
                            data_list_error.append(values)
                        break
            else:
                print(f"Line length is not greater than 3: {values}")

        return data_list, data_list_error
