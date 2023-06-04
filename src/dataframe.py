import copy
from datetime import datetime
import logging
import re
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from src.series import Series

logging.basicConfig(level=logging.INFO)


class DataFrame:
    """
    Ensemble de Serie ayant toutes les mêmes listes d'index
    """

    def __init__(self, **kwargs: dict[str, Any]) -> Any:
        """
        Fonction __init__ permettant de créer une nouvelle instance de la classe DataFrame à partir d'un
        ensemble de Series ou à partir de données et colonnes

        Parameters
        ----------
        kwargs : dict:
            Le dictionnaire de clé: valeur afin de supporter la surchage de constructeur pour le DataFrame
        series : list:
            La liste d'objets de la classe Series
        data : list:
            Une liste de liste où chaque élément correspond à une colonne
        colonnes : list
            La liste des colonnes pour chaque liste de données

        Returns
        -------
        DataFrame
            Nouvel instance de la classe DataFrame
        Raises
        -------
        AttributeError
            Paramètre non conforme
        """

        if kwargs.get("colonnes"):
            if not isinstance(kwargs.get("colonnes"), list):
                logging.exception(
                    f"Type attendu pour le paramètre colonnes : {list}. "
                    f"Type reçu {type(kwargs.get('colonnes'))} ",
                )
                raise AttributeError
            else:
                if len(set(kwargs.get("colonnes"))) != len(kwargs.get("colonnes")):
                    logging.exception("Les colonnes ne sont pas toutes uniques")
                    raise AttributeError
                self.colonnes = kwargs.get("colonnes")

        if kwargs.get("colonnes") and kwargs.get("data"):
            if not isinstance(kwargs.get("data"), list):
                logging.exception(
                    f"Type attendu pour data : {list}. Type reçu : {type(kwargs.get('data'))}"
                )
                raise AttributeError

            # vérifier les tailles
            if len(self.colonnes) != len(kwargs.get("data")):
                logging.exception(
                    f"Le nombre de colonnnes est différent du nombre d'éléments dans data"
                )
                raise AttributeError

            data = []
            for colonne, liste in zip(kwargs.get("colonnes"), kwargs.get("data")):
                data.append(
                    cast_into_most_reccurent_type(liste)
                )  # cast_into_most_reccurent_type(liste))

            self.data = {
                colonne: Series(data=serie, name=colonne)
                for colonne, serie in zip(self.colonnes, data)
            }

        elif kwargs.get("series"):
            series_list = kwargs.get("series")
            if series_list:
                for index, serie in enumerate(series_list):
                    series_list[index].data = cast_into_most_reccurent_type(serie.data)

                self.colonnes = [
                    serie.name if serie.name is not None else f"Unnamed {index}"
                    for (index, serie) in enumerate(series_list)
                ]

                self.data = {
                    colonne: serie for colonne, serie in zip(self.colonnes, series_list)
                }

    def __getitem__(self, index: Tuple[Union[int, slice], Union[int, slice]]) -> Any:
        """
        Fonction permettant de d'indexer l'instance d'une classe, nécessaire pour la propriété iloc

        Parameters
        ----------
        index : tuple:
            Tuple à deux éléments puvant être un slice ou un int


        Returns
        -------
        DataFrame ou Series
            Nouvel objet de type Series ou DataFrame indexée

        Raises
        ------
        IndexError
            Paramètre index non conforme.
        """
        if not isinstance(index, tuple):
            logging.exception("Mauvais type d'index")
            raise IndexError(
                f"Type d'index attendu : {tuple}. Type reçu : {type(index)}"
            )
        row_start = None
        column_start = None
        row_stop = None
        column_stop = None

        if isinstance(index[0], slice):
            row_start = index[0].start
            row_stop = index[0].stop
        elif isinstance(index[0], int):
            row_start = index[0]
        if isinstance(index[1], slice):
            column_start = index[1].start
            column_stop = index[1].stop
        elif isinstance(index[1], int):
            column_start = index[1]

        is_integer_and_integer = isinstance(index[0], int) and isinstance(index[1], int)
        is_slice_and_integer = isinstance(index[0], slice) and isinstance(index[1], int)
        is_integer_and_slice = isinstance(index[0], int) and isinstance(index[1], slice)
        is_slice_and_slice = isinstance(index[0], slice) and isinstance(index[1], slice)

        if is_integer_and_integer:
            return list(self.data.values())[column_start].data[row_start]
        elif is_slice_and_integer:
            return Series(
                data=list(self.data.values())[column_start].data[row_start:row_stop],
                name=list(self.data.keys())[column_start],
            )
        elif is_integer_and_slice:
            data = [d.data[row_start] for d in self.data.values()]
            columns = self.colonnes[column_start:column_stop]
            series = [Series(data=[val], name=name) for val, name in zip(data, columns)]
            return DataFrame(series=series)
        elif is_slice_and_slice:
            data = [d.data[row_start:row_stop] for d in self.data.values()]
            columns = self.colonnes[column_start:column_stop]
            series = [
                Series(
                    data=[series_data]
                    if not isinstance(series_data, list)
                    else series_data,
                    name=series_name,
                )
                for series_data, series_name in zip(data, columns)
            ]
            return DataFrame(series=series)

    @property
    def iloc(self):
        """
        Propriété de la classe DataFrame permettant une indexation basée sur la position des éléments

        Returns
        -------
        DataFrame
            L'instance par laquelle la méthode est appelée
        """
        return self

    def count(self) -> Any:
        """
        Récupère le nombre d'élements présent dans une Serie

        Returns
        -------
        int
            Le nombre d'éléments du DataFrame
        """
        return self.data.get(list(self.data.keys())[0]).count()

    def min(self) -> Any:
        """
        Récupère le plus petit élement numérique de chaque Serie composant
        un DataFrame

        Returns
        -------
        DataFrame
            L'élement le plus petit pour chaque colonne
        """

        minimums = [
            Series(data=[element.min()], name=name)
            for name, element in self.data.items()
        ]
        return DataFrame(series=minimums)

    def max(self) -> Any:
        """
        Récupère le plus grand élement numérique de chaque Serie composant
        un DataFrame

        Returns
        -------
        DataFrame
            L'élement le plus grand pour chaque colonne
        """
        maximums = [
            Series(data=[element.max()], name=name)
            for name, element in self.data.items()
        ]
        return DataFrame(series=maximums)

    def mean(self) -> Any:
        """
        Calcul de la moyenne de l'ensemble des colonnes d'une dataframe

        Returns
        -------
        DataFrame
            La moyenne pour chaque colonne

        Raises
        -------
        ValueError
            Une des Series n'a pas d'éléments numérique
        """
        moyennes = [
            Series(data=[element.mean()], name=name)
            for name, element in self.data.items()
        ]
        return DataFrame(series=moyennes)

    def std(self) -> Any:
        """
        Calcul de l'écart-type de l'ensemble des colonnes d'une dataframe

        Returns
        -------
        DataFrame
            L'écart-type pour chaque colonne

        Raises
        -------
        ValueError
            Une des Series n'a pas d'éléments numérique
        """
        stds = [
            Series(data=[element.std()], name=name)
            for name, element in self.data.items()
        ]
        return DataFrame(series=stds)

      
    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]) -> Any:
        """
        Permet de combiner et d'agréger plusieurs lignes d'un DataFrame en formant des groupes à partir d'une
        ou plusieurs colonnes.

        Parameters
        -------

        by: str:
            Le nom de la ou des colonnes sur lesquelles grouper
        agg: dict:
            La stratégie d'agrégation des colonnes
        Returns
        -------
        DataFrame
            Nouvelle instance de DataFrame contenant les valeurs aggrégés
        """

        if not isinstance(by, (list, str)):
            raise Exception

        is_in_list = [True if element in self.colonnes else False for element in by]

        if False in is_in_list:
            raise ValueError
        else:
            series_list = []
            doublon_indexes = []
            for colonne in by:
                if colonne in agg:
                    # Regarder les valeurs uniques de la colonne sélectionné lors du by
                    doublons = {}
                    for index, valeur in enumerate(self.data.get(colonne).data):
                        if valeur in doublons:
                            doublons[valeur].append(index)
                        else:
                            doublons[valeur] = [index]

                    # Crée la série de colonne du by et qui est dans agg et l'ajoute dans la liste des series
                    datas = []
                    for d in list(doublons.values()):
                        values = []
                        if len(d) == 1:
                            datas.append(self.iloc[d[0], self.colonnes.index(colonne)])
                        else:
                            doublon_indexes.append(d)
                            for d_index in d:
                                # récupère une valeur unique
                                values.append(
                                    self.iloc[d_index, self.colonnes.index(colonne)]
                                )
                            datas.append(values[0])

                    series_list.append(Series(data=datas, name=colonne))

            # Parcours les colonnes à part la colonne du by et crée une nouvelle serie avec sum appliqué
            for col in self.colonnes:
                if col not in by:
                    datas = []
                    doublon_values = []
                    for group_indexes in doublon_indexes:
                        for index in group_indexes:
                            doublon_values.append(
                                self.iloc[index, self.colonnes.index(col)]
                            )

                    for agg_value in agg.values():
                        # datas.append(agg_value(doublon_values))
                        if agg_value == sum:
                            is_float_or_int = all(
                                [isinstance(el, (float, int)) for el in doublon_values]
                            )
                            if is_float_or_int:
                                datas.append(agg[by[0]](doublon_values))
                            else:
                                datas.append("".join(doublon_values))

                            datas += [
                                self.iloc[i, self.colonnes.index(col)]
                                for i in range(self.data.get(col).count())
                                if i not in doublon_indexes[0]
                            ]

                        if agg_value == max or agg_value == min:
                            datas.append(agg_value(doublon_values))

                            datas += [
                                self.iloc[i, self.colonnes.index(col)]
                                for i in range(self.data.get(col).count())
                                if i not in doublon_indexes[0]
                            ]

                    series_list.append(Series(data=datas, name=col))

            # TODO : Retourner une exception si la fonction d'aggrégation n'est pas possible pour la fonction appelé
            # Créer un nouveau dataframe à partir de chaque nouvelle colonne
            new_dataframe = DataFrame(series=series_list)
            # Retourner cet instance nouvellement créée
            return new_dataframe

    def join(
            self,
            other,
            left_on: List[str] | str,
            right_on: List[str] | str,
            how: str = "left",
    ) -> Any:

        """
        Permet de combiner des données provenant de deux DataFrames

        Parameters
        -------
        other: DataFrame:
            Une instance de la classe DataFrame
        left_on : List | str: Le nom de la ou des colonnes de la dataframe de gauche ``self``
        right_on : List | str: Le nom de la ou des colonnes de la dataframe de droite ``other``
        how : str: La manière dont la jointure sera faite ``à gauche, à droite, intérieures et pleines``

        Returns
        -------
        DataFrame
            Le nouvel objet DataFrame ayant été combiné avec une l'autre dataframe
        """
        if not isinstance(other, DataFrame):
            logging.log(
                logging.CRITICAL,
                f"Type attendu pour other : {DataFrame}. Got {type(other)}",
            )
        how_list = ["left", "right", "inner", "outer"]
        if not isinstance(left_on, (list, str)) and not isinstance(
            right_on, (list, str)
        ):
            logging.log(logging.CRITICAL, "Argument left_on ou right_on non conformes")
        if how not in how_list:
            logging.log(
                logging.CRITICAL,
                f"Argument attendu pour how : {' ou '.join(how_list)}. Got {type(other)}",
            )

        result = []

        # Vérification des types des clés
        if isinstance(left_on, str):
            left_on = [left_on]
        if isinstance(right_on, str):
            right_on = [right_on]

        def add_suffix(col: str, i: int, df: DataFrame, suffix: str):
            """
            Fonction utilitaire permettant d'ajouter un suffixe
            sur le dataframe de gauche ou droite en fonction de sa présence
            """
            df.colonnes[i] = col + suffix
            df.data.get(col).set_name(col + suffix)
            df.data[col + suffix] = df.data.get(col)
            del df.data[col]

        if how == "left":
            left_dataframe = copy.deepcopy(self)
            unique_right_cols = []
            for index, colonne in enumerate(other.colonnes):
                if colonne in left_dataframe.colonnes:
                    add_suffix(colonne, index, other, "_y")
                    add_suffix(colonne, index, left_dataframe, "_x")
                else:
                    unique_right_cols.append(other.data.get(colonne))

            right_series_empty = []
            for serie in other:
                if "_y" in serie.name:
                    right_series_empty.append(Series(data=[None] * serie.count(), name=serie.name))
            right_series_empty.extend(unique_right_cols)
            left_series = list(left_dataframe.data.values())
            return DataFrame(series=left_series + right_series_empty)
        if how == "right":
            left_dataframe = copy.deepcopy(self)
            unique_right_cols = []
            for index, colonne in enumerate(other.colonnes):
                if colonne in left_dataframe.colonnes:
                    add_suffix(colonne, index, other, "_y")
                    add_suffix(colonne, index, left_dataframe, "_x")
                else:
                    unique_right_cols.append(other.data.get(colonne))
            left_series_empty = []
            for serie in left_dataframe:
                if "_x" in serie.name:
                    left_series_empty.append(Series(data=[None] * serie.count(), name=serie.name))
            right_series = list(other.data.values())
            right_series.append(right_series.pop(0))
            return DataFrame(series=left_series_empty + right_series)

    def __str__(self) -> str:
        """
        Redéfinition de la méthode __str__ permettant de formatter l'affichage de l'instance d'une classe DataFrame

        Returns
        -------
        str
            Une chaîne de caractères correspondant à l'instance de la classe DataFrame
        """
        data = [d.data for d in self.data.values()]
        p = "\t".join(self.colonnes)
        for index, element in enumerate(zip(*data)):
            p += "\n"
            p += (
                    str(index)
                    + " "
                    + "   ".join(str(item).ljust(len(self.colonnes)) for item in element)
            )
        return p

    def __iter__(self) -> Any:
        """
        Redéfinition de la méthode __iter__ permettant d'itérer sur chaque série composant un DataFrame
        Returns
        -------
        DataFrame
            self (L'instance par laquelle la méthode a été appelée)
        """
        self.index = 0
        return self

    def __next__(self) -> Any:
        """
        Redéfinition de la méthode __next__ permettant de passer à la série suivante d'un DataFrame
        Raises
        -------
        StopIteration
            Arrêt de la boucle lorsque l'index est supérieur au nombre d'éléments
        """
                str(index)
                + " "
                + "   ".join(str(item).ljust(len(self.colonnes)) for item in element)
            )
        return p


    def __len__(self) -> int:
        """
        Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe DataFrame

        Returns
        -------
        int
            Le nombre d'élements
        """
        return self.count()

    def __eq__(self, other) -> bool:
        """
        Redéfinition de la méthode __eq__ permettant de comparer deux instances de la classe DataFrame

        Returns
        -------
        bool
            True or False
        """
        if len(self) != len(other):
            return False
        elif self.colonnes != other.colonnes:
            return False
        for self_serie, other_serie in zip(self, other):
            if self_serie != other_serie:
                return False

        return True


def cast_into_most_reccurent_type(elements: List) -> List:
    types = []
    list_types = []
    for element in elements:
        if re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", str(element)):
            types.append(type(datetime.strptime(element, "%d-%m-%Y").date()))
        else:
            types.append(type(element))
        occurences = dict(list(set(map(lambda x: (x, types.count(x)), types))))
        type_max = None
        for cle, valeur in occurences.items():
            if valeur == max(list(occurences.values())):
                type_max = cle
        values = []
        for index, el in enumerate(elements):
            try:
                if re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", str(el)):
                    values.append(datetime.strptime(el, "%d-%m-%Y").date())
                elif el is None:
                    values.append(None)
                else:
                    values.append(type_max.__new__(type_max, el))
            except ValueError:
                values.append(None)
        elements.append(values)
        list_types.append(types)
        return values
