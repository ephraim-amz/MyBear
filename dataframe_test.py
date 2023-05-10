import unittest

from mybear import Series, DataFrame
import numpy as np


class DataFrameTest(unittest.TestCase):
    """
        Classe regroupant les tests unitaires de la classe DataFrame du module mybear
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
            Méthode permettant de créer une instance de classe commune pour tous les tests
            :param cls: Référence à la classe qui sera instanciée
            :return: None
        """
        first_serie = Series({'a': 1, 'b': 2}, name='a')
        second_serie = Series({'a': 3, 'b': 4}, name='b')
        # cls.df = DataFrame(colonnes=['a', 'b'], data=[[1, 3], [9, 4]])
        cls.df = DataFrame(first_serie, second_serie)

    def test_min(self):
        """
            Test case permettant de vérifier la validité de la fonction min() de la classe DataFrame
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df.min(), [1, 3])

    def test_max(self):
        """
            Test case permettant de vérifier la validité de la fonction max() de la classe DataFrame
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df.max(), [9, 4])

    def test_min_inferior_to_max(self):
        """
            Test case permettant de vérifier que la fonction min() retourne une valeur inférieure à la fonction max()
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertLess([1, 2], [3, 4])

    def test_count(self):
        """
            Test case permettant de vérifier que la fonction  count() retourne le nombre d'élements d'une série
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df.count(), 2)

    def test_std(self):
        """
            Test case permettant de vérifier que la fonction std() de la classe DataFrame retourne la bonne valeur pour l'écart-type
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df.std(), [4.0, 0.5])

    def test_mean(self):
        """
            Test case permettant de vérifier que la fonction std() de la classe DataFrame retourne la bonne valeur pour la moyenne
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df.mean(), [5, 3.5])

    def test_groupby(self):
        with self.assertRaises(NotImplementedError):
            self.df.groupby(by=None, agg=None)

    def test_join(self):
        with self.assertRaises(NotImplementedError):
            self.df.join(other=None, right_on=None, left_on=None)


if __name__ == '__main__':
    unittest.main()
