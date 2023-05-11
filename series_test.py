import unittest

from mybear import Series
import numpy as np


class SeriesTest(unittest.TestCase):
    """
        Classe regroupant les tests unitaires de la classe Serie du module mybear
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
            Méthode permettant de créer une instance de classe commune pour tous les tests
            :param cls: Référence à la classe qui sera instanciée
            :return: None
        """
        cls.serie = Series(range(10), name='Test')

    def test_min(self) -> None:
        """
            Test case permettant de vérifier la validité de la méthode min() de la classe Series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(np.min(self.serie.data), self.serie.min())

    def test_max(self) -> None:
        """
            Test case permettant de vérifier la validité de la méthode max() de la classe Series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(np.max(self.serie.data), self.serie.max())

    def test_min_inferior_to_max(self) -> None:
        """
            Test case permettant de vérifier que la méthode min() retourne une valeur inférieure à la méthode max()
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertLess(self.serie.min(), self.serie.max())

    def test_count(self) -> None:
        """
            Test case permettant de vérifier que la méthode count() retourne le nombre d'élements d'une série
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(len(self.serie.data), self.serie.count())

    def test_std(self) -> None:
        """
            Test case permettant de vérifier que la méthode std() de la classe Series retourne la bonne valeur pour l'écart-type
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(np.std(self.serie.data), self.serie.std())

    def test_mean(self) -> None:
        """
            Test case permettant de vérifier que la méthode std() de la classe Series retourne la bonne valeur pour la moyenne
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(np.mean(self.serie.data), self.serie.mean())


if __name__ == '__main__':
    unittest.main()
