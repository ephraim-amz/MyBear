import unittest

from mybear import Series, DataFrame, read_json, read_csv
import numpy as np


class DataFrameTest(unittest.TestCase):
    """
        Classe regroupant les tests unitaires de la classe DataFrame du module mybear
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
            Méthode de clase permettant de créer des variables qui seront utilisés pour tous les tests
            :param cls: Référence à la classe qui sera instanciée
            :return: None
        """
        first_serie = Series([1, 3], name='a')
        second_serie = Series([2, 4], name='b')
        cls.df_colonnes = DataFrame(colonnes=['a', 'b'], data=[[1, 3], [2, 4]])
        cls.df_series = DataFrame(series=[first_serie, second_serie])

    def test_min_colonnes(self):
        """
            Test case permettant de vérifier la validité de la méthode min() de l'instance de la classe DataFrame
            initialisée
            avec le constructeur colonnes
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.min(element.data) for element in self.df_colonnes.data.values()], self.df_colonnes.min())

    def test_min_series(self):
        """
            Test case permettant de vérifier la validité de la méthode min() de l'instance de la classe DataFrame
            initialisée avec le constructeur series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.min(element.data) for element in self.df_series.data.values()], self.df_series.min())

    def test_minimums_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `min()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.min(), self.df_colonnes.min())

    def test_max_series(self):
        """
            Test case permettant de vérifier la validité de la méthode max() de l'instance de la classe DataFrame
            initialisée avec le constructeur series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.max(element.data) for element in self.df_series.data.values()], self.df_series.max())

    def test_max_colonnes(self):
        """
            Test case permettant de vérifier la validité de la méthode max() de l'instance de la classe DataFrame
            initialisée avec le constructeur colonnes
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.max(element.data) for element in self.df_colonnes.data.values()], self.df_colonnes.max())

    def test_maximums_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `max()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.max(), self.df_colonnes.max())

    def test_min_inferior_to_max(self):
        """
            Test case permettant de vérifier que la méthode min() retourne une valeur inférieure à la méthode max()
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertLess(self.df_colonnes.min(), self.df_colonnes.max())
        self.assertLess(self.df_series.min(), self.df_series.max())

    def test_count_series(self):
        """
            Vérification de la méthode count() pour un dataframe initialisé avec une liste de series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(len(self.df_series.data), self.df_series.count())

    def test_count_colonnes(self):
        """
            Test case permettant de vérifier que la méthode pour un dataframe initialisé avec les colonnes et données
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(len(self.df_colonnes.data), self.df_colonnes.count())

    def test_count_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `count()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.count(), self.df_colonnes.count())

    def test_std_series(self):
        """
            Vérification de l'écart-type pour une dataframe initialisé avec une liste de series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.std(element.data) for element in self.df_series.data.values()], self.df_series.std())

    def test_std_colonnes(self):
        """
            Vérification de l'écart-type pour une dataframe initialisé avec les colonnes + données
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.std(element.data) for element in self.df_colonnes.data.values()], self.df_colonnes.std())

    def test_std_equals(self):
        self.assertEqual(self.df_series.std(), self.df_colonnes.std())

    def test_mean_colonnes(self):
        """
            Test case permettant de vérifier que la méthode mean() de la classe DataFrame retourne la bonne valeur
            pour la moyenne
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.mean(element.data) for element in self.df_colonnes.data.values()], self.df_colonnes.mean())

    def test_mean_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `mean()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.mean(), self.df_colonnes.mean())

    def test_mean_series(self):
        """
            Vérification de la moyenne pour une dataframe initialisé à partir d'une liste de series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual([np.mean(element.data) for element in self.df_series.data.values()], self.df_series.mean())

    def test_groupby(self):
        with self.assertRaises(Exception):
            self.df_colonnes.groupby(by=None, agg=None)

    def test_join(self):
        with self.assertRaises(Exception):
            self.df_colonnes.join(other=None, right_on=None, left_on=None)

    def test_same_data_json_orient(self):
        df_orient_records = read_json(path="oriented_records.json")
        df_orient_columns = read_json(path="oriented_columns.json", orient="columns")
        self.assertEqual([v.data for v in df_orient_columns.data.values()],
                         [v.data for v in df_orient_columns.data.values()])
        self.assertEqual(df_orient_columns.colonnes, df_orient_records.colonnes)


if __name__ == '__main__':
    unittest.main()
