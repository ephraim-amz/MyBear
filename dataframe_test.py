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
        minimum_colonnes = [Series(data=[np.max(element.data)], name=name) for name, element in
                            self.df_colonnes.data.items()]
        self.assertEqual(DataFrame(series=minimum_colonnes).__repr__(), self.df_colonnes.max().__repr__())

    def test_min_series(self):
        """
            Test case permettant de vérifier la validité de la méthode min() de l'instance de la classe DataFrame
            initialisée avec le constructeur series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        minimum_series = [Series(data=[np.max(element.data)], name=name) for name, element in
                          self.df_series.data.items()]
        self.assertEqual(DataFrame(series=minimum_series).__repr__(), self.df_series.max().__repr__())

    def test_minimums_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `min()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.min().__repr__(), self.df_colonnes.min().__repr__())

    def test_max_series(self):
        """
            Test case permettant de vérifier la validité de la méthode max() de l'instance de la classe DataFrame
            initialisée avec le constructeur series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        maximums_colonnes = [Series(data=[np.max(element.data)], name=name) for name, element in
                             self.df_series.data.items()]
        self.assertEqual(DataFrame(series=maximums_colonnes).__repr__(), self.df_series.max().__repr__())

    def test_max_colonnes(self):
        """
            Test case permettant de vérifier la validité de la méthode max() de l'instance de la classe DataFrame
            initialisée avec le constructeur colonnes
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        maximums_series = [Series(data=[np.max(element.data)], name=name) for name, element in
                           self.df_colonnes.data.items()]
        self.assertEqual(DataFrame(series=maximums_series).__repr__(), self.df_colonnes.max().__repr__())

    def test_maximums_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `max()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.max().__repr__(), self.df_colonnes.max().__repr__())

    def test_min_inferior_to_max(self):
        """
            Test case permettant de vérifier que la méthode min() retourne une valeur inférieure à la méthode max()
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertLess(self.df_colonnes.min().__repr__(), self.df_colonnes.max().__repr__())
        self.assertLess(self.df_series.min().__repr__(), self.df_series.max().__repr__())

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
        std_series = [Series(data=[np.std(element.data)], name=name) for name, element in
                      self.df_series.data.items()]
        self.assertEqual(DataFrame(series=std_series).__repr__(), self.df_series.std().__repr__())

    def test_std_colonnes(self):
        """
            Vérification de l'écart-type pour une dataframe initialisé avec les colonnes + données
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        std_colonnes = [Series(data=[np.std(element.data)], name=name) for name, element in
                        self.df_colonnes.data.items()]
        self.assertEqual(DataFrame(series=std_colonnes).__repr__(), self.df_colonnes.std().__repr__())

    def test_std_equals(self):
        self.assertEqual(self.df_series.std().__repr__(), self.df_colonnes.std().__repr__())

    def test_mean_colonnes(self):
        """
            Test case permettant de vérifier que la méthode mean() de la classe DataFrame retourne la bonne valeur
            pour la moyenne
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        mean_colonnes = [Series(data=[np.mean(element.data)], name=name) for name, element in
                         self.df_colonnes.data.items()]
        self.assertEqual(DataFrame(series=mean_colonnes).__repr__(), self.df_colonnes.mean().__repr__())

    def test_mean_equals(self):
        """
            Test case permettant de vérifier qu'un dataframe initialisé avec une liste
            et un autre initialisé avec colonnes + valeurs renvoyent la même valeur pour la méthode `mean()`
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        self.assertEqual(self.df_series.mean().__repr__(), self.df_colonnes.mean().__repr__())

    def test_mean_series(self):
        """
            Vérification de la moyenne pour une dataframe initialisé à partir d'une liste de series
            :param self: Référence à l'instance par laquelle la méthode est appelée
            :return: None
        """
        mean_series = [Series(data=[np.mean(element.data)], name=name) for name, element in
                       self.df_series.data.items()]
        self.assertEqual(DataFrame(series=mean_series).__repr__(), self.df_series.mean().__repr__())

    def test_groupby(self):
        with self.assertRaises(Exception):
            self.df_colonnes.groupby(by="price", agg={"price": min})

    def test_join(self):
        with self.assertRaises(Exception):
            self.df_colonnes.join(other=self.df_series, right_on="price", left_on="date")

    def test_same_data_json_orient(self):
        df_orient_records = read_json(path="oriented_records.json")
        df_orient_columns = read_json(path="oriented_columns.json", orient="columns")
        self.assertEqual([v.data for v in df_orient_columns.data.values()],
                         [v.data for v in df_orient_records.data.values()])
        self.assertEqual(df_orient_columns.colonnes, df_orient_records.colonnes)
        self.assertEqual(df_orient_columns.__repr__(), df_orient_records.__repr__())


if __name__ == '__main__':
    unittest.main()
