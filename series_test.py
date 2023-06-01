from mybear import Series
import numpy as np
import pytest


@pytest.fixture
def serie():
    return Series(range(10), name="Test")


def test_min(serie) -> None:
    """
    Test case permettant de vérifier la validité de la méthode min() de la classe Series
    :param serie: Référence à l'instance par laquelle la méthode est appelée
    :return: None
    """
    assert np.min(serie.data) == serie.min()


def test_max(serie) -> None:
    """
    Test case permettant de vérifier la validité de la méthode max() de la classe Series
    :param serie: Référence à l'instance par laquelle la méthode est appelée
    :return: None
    """
    assert np.max(serie.data) == serie.max()


def test_min_inferior_to_max(serie) -> None:
    """
    Test case permettant de vérifier que la méthode min() retourne une valeur inférieure à la méthode max()
    :param serie: Référence à l'instance par laquelle la méthode est appelée
    :return: None
    """
    assert serie.min() < serie.max()


def test_count(serie) -> None:
    """
    Test case permettant de vérifier que la méthode count() retourne le nombre d'élements d'une série
    :param serie: Référence à l'instance par laquelle la méthode est appelée
    :return: None
    """
    assert len(serie.data) == serie.count()


def test_std(serie) -> None:
    """
    Test case permettant de vérifier que la méthode std() de la classe Series retourne la bonne valeur
    pour l'écart-type
    :param serie: Référence à l'instance par laquelle la méthode est appelée
    :return: None
    """
    assert np.std(serie.data) == serie.std()


def test_mean(serie) -> None:
    """
    Test case permettant de vérifier que la méthode std() de la classe Series retourne la bonne valeur
    pour la moyenne
    :param serie: Référence à l'instance par laquelle la méthode est appelée
    :return: None
    """
    assert np.mean(serie.data) == serie.mean()


def test_equals(serie):
    assert serie == Series(range(10), name="Test")
