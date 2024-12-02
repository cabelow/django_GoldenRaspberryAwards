import logging
import sys
import os
import pytest
from Core.Movies.service import ImportMovieCSVService, MovieService
from Core.Movies.models import Movie, Producer, Studio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

@pytest.mark.django_db(transaction=True)
def setup_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "import_csv_test.csv")
    assert os.path.exists(file_path), "Arquivo CSV não encontrado na pasta do teste"
    os.chmod(file_path, 0o644)

    with open(file_path, "rb") as file:
        ImportMovieCSVService.process_file(file)

@pytest.mark.django_db(transaction=True)
def test_get_all_movies():
    setup_data()
    result = MovieService.get_all_movies(filters={}, page=1, size=10)
    logger.info("Resultado da consulta: %s", result)
    assert result['content']
    assert len(result['content']) > 0

@pytest.mark.django_db(transaction=True)
def test_get_years_with_multiple_winners():
    setup_data()
    years = MovieService.get_years_with_multiple_winners()
    logger.info("Anos com múltiplos vencedores: %s", years)
    assert isinstance(years, list)
    assert all(isinstance(entry, dict) and 'year' in entry and isinstance(entry['year'], int) for entry in years)

@pytest.mark.django_db(transaction=True)
def test_get_studios_with_winners():
    setup_data()
    result = MovieService.get_studios_with_winners()
    logger.info("Estúdios com vitórias: %s", result)
    assert isinstance(result, dict)
    assert 'studios' in result
    assert isinstance(result['studios'], list)
    for studio in result['studios']:
        assert isinstance(studio, dict)
        assert 'name' in studio and isinstance(studio['name'], str)
        assert 'winCount' in studio and isinstance(studio['winCount'], int)

@pytest.mark.django_db(transaction=True)
def test_get_producers_with_winner_intervals():
    setup_data()
    result = MovieService.get_producers_with_winner_intervals()
    logger.info("Produtores com intervalos de vencedores: %s", result)
    assert isinstance(result, dict)
    assert "min" in result and "max" in result
    assert isinstance(result["min"], list)
    assert isinstance(result["max"], list)
    assert len(result["min"]) > 0
    assert len(result["max"]) > 0

@pytest.mark.django_db(transaction=True)
def test_get_movies_with_winner():
    setup_data()
    filters = {"winner": "true", "year": 1986}
    result = MovieService.get_movies_with_winner(filters)
    logger.info("Resultado de get_movies_with_winner: %s", result)
    assert isinstance(result, list)
    assert len(result) > 0
    for movie in result:
        assert isinstance(movie, dict)
        assert "title" in movie and isinstance(movie["title"], str)
        assert "year" in movie and isinstance(movie["year"], int)
        assert "winner" in movie and isinstance(movie["winner"], bool)
        assert "producer_name" in movie and isinstance(movie["producer_name"], list)
        assert all(isinstance(producer, str) for producer in movie["producer_name"])
        assert "studio_name" in movie and isinstance(movie["studio_name"], list)
        assert all(isinstance(studio, str) for studio in movie["studio_name"])
