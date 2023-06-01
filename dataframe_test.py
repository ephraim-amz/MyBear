from mybear import DataFrame
from mybear import read_json
from mybear import Series
import numpy as np
import pytest


@pytest.fixture
def first_serie() -> Series:
    return Series(range(5), name="a")


@pytest.fixture
def second_serie() -> Series:
    return Series(range(4), name="b")


@pytest.fixture
def df_series() -> DataFrame:
    """
    Méthode de clase permettant de créer des variables qui seront
    utilisés pour tous les tests

    """
    first_serie = Series(range(5), name="a")
    second_serie = Series(range(4), name="b")

    return DataFrame(
        series=[first_serie, second_serie]
    )


@pytest.fixture
def df_colonnes() -> DataFrame:
    return DataFrame(
        colonnes=["a", "b"], data=[[0, 1, 2, 3, 4], [0, 1, 2, 3]]
    )


def test_min_colonnes(df_colonnes):
    """
    Test case permettant de vérifier la validité de la méthode min() de
    l'instance de la classe DataFrame initialisée avec le constructeur
    colonnes
    """
    minimum_colonnes = [
        Series(data=[np.min(element.data)], name=name)
        for name, element in df_colonnes.data.items()
    ]

    assert DataFrame(series=minimum_colonnes) == df_colonnes.min()


def test_min_series(df_series):
    """
    Test case permettant de vérifier la validité de la méthode min() de
    l'instance de la classe DataFrame
    initialisée avec le constructeur series
    """
    minimum_series = [
        Series(data=[np.max(element.data)], name=name)
        for name, element in df_series.data.items()
    ]
    assert DataFrame(series=minimum_series) == df_series.max()


def test_minimums_equals(df_series, df_colonnes):
    """
    Test case permettant de vérifier qu'un dataframe initialisé avec une
    liste et un autre initialisé avec colonnes + valeurs renvoyent la même
    valeur pour la méthode `min()`
    """
    assert df_series.min() == df_colonnes.min()


def test_max_series(df_series):
    """
    Test case permettant de vérifier la validité de la méthode max() de
    l'instance de la classe DataFrame initialisée avec le constructeur
    series
    """
    maximums_colonnes = [
        Series(data=[np.max(element.data)], name=name)
        for name, element in df_series.data.items()
    ]
    assert DataFrame(series=maximums_colonnes) == df_series.max()


def test_max_colonnes(df_colonnes):
    """
    Test case permettant de vérifier la validité de la méthode max() de
    l'instance de la classe DataFrame initialisée avec le constructeur
    colonnes
    """
    maximums_series = [
        Series(data=[np.max(element.data)], name=name)
        for name, element in df_colonnes.data.items()
    ]
    assert DataFrame(series=maximums_series) == df_colonnes.max()


def test_maximums_equals(df_colonnes, df_series):
    """
    Test case permettant de vérifier qu'un dataframe initialisé avec
    une liste et un autre initialisé avec colonnes + valeurs
    renvoyent la même valeur pour la méthode `max()`
    """
    assert df_series.max() == df_colonnes.max()


def test_min_inferior_to_max(df_colonnes, df_series):
    """
    Test case permettant de vérifier que la méthode min() retourne une
    valeur inférieure à la méthode max()
    """
    assert df_colonnes.min() < df_colonnes.max()
    assert df_series.min() < df_series.max()


def test_count_series(df_colonnes, df_series):
    """
    Vérification de la méthode count() pour un dataframe initialisé avec
    une liste de series
    """
    assert len(df_series) == df_series.count()


def test_count_colonnes(df_colonnes, df_series):
    """
    Test case permettant de vérifier que la méthode pour un dataframe
    initialisée avec les colonnes et données
    """
    assert len(df_colonnes) == df_colonnes.count()


def test_count_equals(df_series, df_colonnes):
    """
    Test case permettant de vérifier qu'un dataframe initialisé avec une
    liste et un autre initialisé avec colonnes + valeurs renvoyent la même
    valeur pour la méthode `count()`
    """
    df_series.count() == df_colonnes.count()


def test_std_series(df_series):
    """
    Vérification de l'écart-type pour une dataframe initialisé avec une
     liste de series
    """
    std_series = [
        Series(data=[np.std(element.data)], name=name)
        for name, element in df_series.data.items()
    ]

    assert DataFrame(series=std_series).data == df_series.std().data


def test_std_colonnes(df_colonnes):
    """
    Vérification de l'écart-type pour une dataframe initialisé avec les
     colonnes + données
    """
    std_colonnes = [
        Series(data=[np.std(element.data)], name=name)
        for name, element in df_colonnes.data.items()
    ]

    assert DataFrame(series=std_colonnes) == df_colonnes.std()


def test_std_equals(df_series, df_colonnes):
    """
    Vérification de l'écart-type pour une dataframe initialisé avec les
    colonnes + données
    """

    df_series.std() == df_colonnes.std()


def test_mean_colonnes(df_colonnes):
    """
    Test case permettant de vérifier que la méthode mean() de la classe
    DataFrame retourne la bonne valeur
    pour la moyenne
    """
    mean_colonnes = [
        Series(data=[np.mean(element.data)], name=name)
        for name, element in df_colonnes.data.items()
    ]
    assert DataFrame(series=mean_colonnes) == df_colonnes.mean()


def test_mean_equals(df_series, df_colonnes):
    """
    Test case permettant de vérifier qu'un dataframe initialisé avec une
    liste et un autre initialisé avec colonnes + valeurs renvoyant la même
    valeur pour la méthode `mean()`
    """

    assert df_series.mean() == df_colonnes.mean()


def test_mean_series(df_series):
    """
    Vérification de la moyenne pour une dataframe initialisée
    à partir d'une liste de series
    """
    mean_series = [
        Series(data=[np.mean(element.data)], name=name)
        for name, element in df_series.data.items()
    ]
    assert DataFrame(series=mean_series) == df_series.mean()


@pytest.mark.skip()
def test_groupby(df_colonnes):
    """
    Vérification de la méthode groupby
    """
    df_colonnes.groupby(by="price", agg={"price": min})


@pytest.mark.skip()
def test_join(df_colonnes, df_series):
    """
    Vérification de la méthode groupby
    """
    df_colonnes.join(other=df_series, right_on="price", left_on="date")


def test_same_data_json_orient():
    """
    Vérification de la méthode groupby
    """
    df_orient_records = read_json(path="oriented_records.json")
    df_orient_columns = read_json(
        path="oriented_columns.json",
        orient="columns")
    assert [v.data for v in df_orient_columns.data.values()] == [v.data for v in df_orient_records.data.values()]
    assert df_orient_columns.colonnes == df_orient_records.colonnes

    assert df_orient_columns == df_orient_records


def test_iloc_series_unique_value(first_serie):
    """
    Vérification de la méthode iloc renvoyant une seule valeur
    """
    assert first_serie.data[1] == first_serie.iloc[1]


def test_iloc_series_slice(first_serie):
    """
    Vérification de la méthode iloc renvoyant une seule instance de la
    classe Series
    """
    assert Series(data=range(1, 4), name=first_serie.name) == first_serie.iloc[1:-1]


def test_iloc_dataframe_unique_value(df_series):
    """
    Vérification de la méthode iloc renvoyant un DataFrame ayant une
    seule valeur
    """
    num_col = 1
    row_num = 2

    assert list(df_series.data.values())[num_col].data[row_num] == df_series.iloc[row_num, num_col]


def test_iloc_dataframe_slice_int(df_series):
    """
    Vérification de la méthode iloc renvoyant une instance de la classe
    Series pour une slice de lignes mais une seule colonne
    """
    slice_rows = slice(1, 3)
    num_col = 1

    assert Series(
        data=list(df_series.data.values())[num_col].data[slice_rows],
        name=df_series.colonnes[num_col],
    ) == df_series.iloc[slice_rows, num_col]


def test_iloc_dataframe_int_slice(df_series):
    """
    Vérification de la méthode iloc renvoyant une instance de la classe
    DataFrame ayant une seule ligne pour chaque colonne selectionnée
    """
    row = 1
    slice_cols = slice(0, 2)

    assert DataFrame(data=[[1], [1]], colonnes=["a", "b"]) == df_series.iloc[row, slice_cols]


def test_iloc_dataframe_slice_slice(df_series):
    """
    Vérification de la méthode iloc renvoyant une instance de la classe
    DataFrame ayant plusieurs lignes pour chaque colonne selectionnée
    """
    slice_rows = slice(0, 2)
    slice_cols = slice(0, 2)
    assert DataFrame(data=[[0, 1], [0, 1]], colonnes=["a", "b"]) == df_series.iloc[
        slice_rows, slice_cols]
