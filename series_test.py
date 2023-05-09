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
        cls.serie = Series(range(10), name='Test', index=[chr(i) for i in range(ord('a'), ord(chr(97 + 10 - 1)) + 1)])

    def test_min(self):
        """
            Test case permettant de vérifier la validité de la fonction min() de la classe Series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.serie.min(), np.min(self.serie.data))

    def test_max(self):
        """
            Test case permettant de vérifier la validité de la fonction max() de la classe Series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.serie.max(), np.max(self.serie.data))

    def test_min_inferior_to_max(self):
        """
            Test case permettant de vérifier que la fonction min() retourne une valeur inférieure à la fonction max()
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertLess(self.serie.min(), self.serie.max())

    def test_count(self):
        """
            Test case permettant de vérifier que la fonction  count() retourne le nombre d'élements d'une série
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.serie.count(), len(self.serie.data))

    def test_std(self):
        """
            Test case permettant de vérifier que la fonction std() de la classe Series retourne la bonne valeur pour l'écart-type
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.serie.std(), np.std(self.serie.data))

    def test_mean(self):
        """
            Test case permettant de vérifier que la fonction std() de la classe Series retourne la bonne valeur pour la moyenne
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.serie.mean(), np.mean(self.serie.data))


if __name__ == '__main__':
    unittest.main()
