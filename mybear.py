import numpy as np
import json
import logging
import csv
import os
from typing import List, Any, Union, Dict, Callable, Tuple
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)


class Series:
    """
    Colonne dans un DataFrame qui contient en plus des données,
    une étiquette (un nom), et des informations statistiques déjà
    présentes et calculées automatiquement lors de la création de
    la Serie (taille, nombre de valeurs manquantes et type de données)
    """

    def __init__(self, data: Union[range, List[Union[Any]]],
                 name: str = None) -> None:
        """
        Fonction __init__ permettant de créer une nouvelle instance de la classe Series

        Parameters
        ----------
        data : list:
            Les données qui peuvent être un range ou bien une liste d'élements
        name : str
            Le nom qui sera attribué à la série (Valeur None par défaut)

        Returns
        -------
        Series
            Nouvel objet de type Series

        Raises
        ------
        AttributeError
            Paramètre data non conforme.
        """

        if isinstance(data, range) or isinstance(data, list):
            self.data = list(data)
            self.index = range(len(data))
            self.name = name
        else:
            logging.exception(
                f"Type attendu : {range} ou {list}. Type reçu : {type(data)}"
            )
            raise AttributeError

    def __set_name(self, name: str) -> None:
        """
        Setter permettant de définir l'attribut name de la classe Series

        Parameters
        ----------
        name : str:
            Le futur nom de l'instance Series
        name : str
            Le nom qui sera attribué à la série (Valeur None par défaut)
        """
        self.name = name

    def __getitem__(self, index: Union[slice, int]):
        """
        Fonction permettant de d'indexer l'instance d'une classe, nécessaire pour la propriété iloc

        Parameters
        ----------
        index : slice | int:
            L'index ou le slice d'index qui sera selectionné


        Returns
        -------
        Series
            Nouvel objet de type Series indexée

        Raises
        ------
        AttributeError
            Paramètre index non conforme.
        """

        if isinstance(index, int):
            return self.data[index]
        elif isinstance(index, slice):
            return Series(
                data=self.data[index],
                name=self.name if self.name is not None else "Undefined",
            )
        else:
            logging.exception(
                logging.ERROR, f"Type attendu : {slice} ou {int}. Reçu : {type(index)}"
            )
            raise AttributeError

    @property
    def iloc(self) -> Any:
        """
        Propriété de la classe Series permettant une indexation basée sur la position des éléments

        Returns
        -------
        Series
            L'instance par laquelle la méthode est appelée
        """

        return self

    def count(self) -> Any:
        """
        Récupère le nombre d'élements présent dans une Serie

        Returns
        -------
        int
            Le nombre d'éléments de la serie
        """
        return len(self.data)

    def min(self) -> Any:
        """
        Récupère le plus petit élément présent dans une Serie

        Returns
        -------
        int
            L'élement le plus petit
        """
        if isinstance(self.data, list):
            return min(self.data)

    def max(self) -> Any:
        """
        Récupère le plus grand élément présent dans une Serie

        Returns
        -------
        int
            L'élement le plus grand
        """
        return max(self.data)

    def mean(self) -> Any:
        """
        Récupère la moyenne des éléments d'une Serie

        Returns
        -------
        float
            La moyenne des éléments de l'instance Serie

        Raises
        ------
        Exception
            La série ne contient pas d'éléments numériques
        """

        try:
            return np.mean(self.data)
        except Exception as e:
            logging.exception(
                logging.ERROR, f"La moyenne ne peut pas être calculé car : {e}"
            )
            raise e

    def std(self) -> Any:
        """
        Récupère l'écart-type des éléments d'une Serie

        Returns
        -------
        float
            L'écart-type des éléments de l'instance Serie

        Raises
        ------
        Exception
            La série ne contient pas d'éléments numériques
        """

        try:
            return np.std(self.data)
        except Exception as e:
            logging.exception(
                logging.ERROR, f"L'écart-type ne peut pas être calculé car : {e}"
            )
            raise e

    def __str__(self):
        """
        Redéfinition de la méthode __str__ permettant de formatter l'affichage de l'instance d'une classe Series

        Returns
        -------
        str
            Une chaîne de caractères correspondant à l'instance de la classe Series
        """
        str_builder = ["{}\t{}".format(i, val) for i, val in enumerate(self.data)]
        str_builder.append(f"Name: {self.name}, dtype: {type(self.data[0])}")
        return "\n".join(str_builder)

    def __len__(self):
        """
        Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe Series

        Returns
        -------
        int
            Le nombre d'élements
        """
        return self.count()


class DataFrame:
    """
    Ensemble de Serie ayant toutes les mêmes listes d'index
    """

    def __init__(self, **kwargs):
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

        """

        if kwargs.get("colonnes"):
            if not isinstance(kwargs.get("colonnes"), list):
                logging.log(
                    logging.ERROR,
                    f"Type attendu pour le paramètre colonnes : {list}. "
                    f"Type reçu {type(kwargs.get('colonnes'))} ",
                )
            else:
                self.colonnes = kwargs.get("colonnes")

        if kwargs.get("colonnes") and kwargs.get("data"):
            self.data = {
                colonne: Series(data=serie, name=colonne)
                for colonne, serie in zip(self.colonnes, kwargs.get("data"))
            }

        elif kwargs.get("series"):
            series_list = kwargs.get("series")
            if series_list:
                self.colonnes = [
                    serie.name if serie.name is not None else f"Unnamed {index}"
                    for (index, serie) in enumerate(series_list)
                ]

                self.data = {
                    colonne: serie for colonne, serie in zip(self.colonnes, series_list)
                }

    def __getitem__(self, index: Tuple[Union[int, slice], Union[int, slice]]):
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

    def mean(self):
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

    def std(self):
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

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]):
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
    ):
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

        if how == "left":
            # Parcours des entrées de l'objet self
            for entry_self in self:
                entry_result = entry_self.copy()
                matching_entries = []

                # Parcours des entrées de l'objet other
                for entry_other in other:
                    matching = True
                    # Vérification des correspondances des clés
                    for left_key, right_key in zip(left_on, right_on):
                        if entry_self[left_key] != entry_other[right_key]:
                            matching = False
                            break

                    if matching:
                        matching_entries.append(entry_other)

                if matching_entries:
                    entry_result["matching_entries"] = matching_entries
                else:
                    entry_result["matching_entries"] = []

                result.append(entry_result)

        elif how == "right":
            ...
        elif how == "inner":
            ...
        elif how == "outer":
            ...

        return result

    def __str__(self):
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

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.data.keys()):
            raise StopIteration
        else:
            serie = self.iloc[:, self.index]
            self.index += 1
            return serie

    def __len__(self):
        """
        Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe DataFrame

        Returns
        -------
        int
            Le nombre d'élements
        """
        return self.count()


def read_csv(path: str, delimiter: str = ","):
    """
    Fonction permettant de créer une nouvelle instance de la classe DataFrame à partir d'un fichier csv

    Parameters
    -------
    path: str:
        Le chemin relatif, absolu, ou tout simplement le nom du fichier csv
    delimiter: str:
        Le séparateur d'éléments au sein du fichier `virgule par défaut`

    Returns
    -------
    DataFrame
        Une nouvelle instance de la classe DataFrame à partir des données du fichier


    Raises
    -------
    FileNotFoundError
        Le fichier n'existe pas
    ValueError
        Une erreur de conversion est survenue
    Exception
        Une erreur est survenue durant la lecture du fichier
    """
    if not os.path.exists(path):
        logging.exception(f"Fichier {path} introuvable")
        raise FileNotFoundError

    try:
        with open(path, mode="r") as f:
            reader = csv.reader(f, delimiter=delimiter)
            lines = [f"{delimiter}".join(row).split(delimiter) for row in reader]
            columns = lines[0]
            lines = list(map(list, zip(*lines[1:])))
            for line in lines:
                for index, element in enumerate(line):
                    if element.isdigit() or element.isnumeric():
                        line[index] = int(element)
                    if element[0] == "-" and element[1:].isdigit():
                        line[index] = -int(element[1:])
                    elif (
                        "." in element and element[element.index(".") + 1:].isnumeric()
                    ):
                        try:
                            line[index] = float(element)
                        except ValueError as ve:
                            logging.exception("Value can not be converted to float")
                            raise ve
                    elif re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", element):
                        line[index] = datetime.strptime(element, "%d-%m-%Y").date()

            dataframe = DataFrame(colonnes=columns, data=lines)
    except Exception as e:
        logging.exception(
            f"Une erreur est survenue durant la lecture du fichier car : {e}"
        )
        raise e
    else:
        return dataframe


def read_json(path: str, orient: str = "records"):
    """
    Fonction permettant de créer une nouvelle instance de la classe DataFrame à partir d'un fichier JSON

    Parameters
    -------
    path: str:
        Le chemin relatif, absolu, ou tout simplement le nom du fichier csv
    orient: str:
        L'orientation du fichier JSON `records par défaut`

    Returns
    -------
    DataFrame
        Une nouvelle instance de la classe DataFrame à partir des données du fichier

    Raises
    -------
    TypeError
        Valeur pour l'orientation du fichier JSON invalide
    FileNotFoundError
        Le fichier n'existe pas
    ValueError
        Une erreur de conversion est survenue
    Exception
        Une erreur est survenue durant la lecture du fichier
    """
    if orient != "records" and orient != "columns":
        logging.exception("Valeur pour le paramètre orient non conforme")
        raise TypeError
    if not os.path.exists(path):
        logging.exception(f"Fichier {path} introuvable")
        raise FileNotFoundError

    try:
        with open(path, mode="r") as f:
            json_object = json.load(f)
            if orient == "records":
                json_dataframe = DataFrame(
                    data=[
                        [obj[key] for obj in json_object]
                        for key in list(json_object[0].keys())
                    ],
                    colonnes=list(json_object[0].keys()),
                )
            if orient == "columns":
                json_dataframe = DataFrame(
                    data=[list(v.values()) for v in json_object.values()],
                    colonnes=list(json_object.keys()),
                )
    except Exception as exc:
        logging.exception(
            f"Une erreur est survenue durant la lecture du fichier car : {exc}"
        )
        raise exc
    else:
        return json_dataframe
