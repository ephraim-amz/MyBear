import numpy as np
import json
import logging
import csv
import os
from typing import List, Any, Union, Dict, Callable


class Series:
    """
        Colonne dans un DataFrame qui contient en plus des données, une étiquette (un nom),
        et des informations statistiques déjà présentes et calculées automatiquement
        lors de la création de la Serie (taille, nombre de valeurs manquantes et type de données)
    """

    def __init__(self, data: Union[range, List[Union[Any]]], name: str = None) -> None:
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe Series
            :param data: Les données qui peuvent être un dictionnaire, un range ou bien une liste d'élements de type
            divers
            :param name: Le nom qui sera attribué à la série (Valeur None par défaut)
            :return: Nouvel objet de type Serie
        """
        if isinstance(data, range) or isinstance(data, list):
            self.data = list(data)
            self.index = range(len(data))
            self.name = name

    def __set_name(self, name) -> None:
        self.name = name

    def __getitem__(self, index: Union[List, int]):
        """
            Fonction permettant de d'indexer l'instance d'une classe, nécessaire pour la propriété iloc
            (Fonction non optimale car la notation est object.iloc(index) ou object.iloc([start,stop])
                et non object.iloc[index] object.iloc[start:stop]
            :param index: Index
            :return: Nouvel objet de type Serie indexée
        """
        is_integer_list_with_two_elements = isinstance(index, list) and len(index) == 2 and all(
            isinstance(i, int) for i in index)
        if not isinstance(index, int) and not is_integer_list_with_two_elements:
            logging.log(logging.CRITICAL,
                        f"L'argument passé en paramètre est incorrect.\n"
                        f"Type attendu : {list} ou {int}. Type reçu : {type(index)}")
            raise ValueError
        elif isinstance(index, int):
            sd = Series(data=list(self.data)[index], name=self.name)
            return sd

    @property
    def iloc(self) -> Any:
        """
            Propriété de la classe Series permettant une indexation basée sur la position des éléments
            :raise: IndexError: Si l'index n'est pas un int ou l'index est invalide
            :return: lambda appelant la fonction __getitem__ définit précédemment
        """
        return lambda index: self[index]

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une Serie
          :returns: Le nombre d'éléments le plus grand
        """
        return len(self.data)

    def min(self) -> Any:
        """
          Récupère le plus petit élement numérique d'une Serie
          :returns: L'élement le plus petit
        """
        if isinstance(self.data, dict):
            return min(list(self.data.values()))
        if isinstance(self.data, list):
            return min(self.data)

    def max(self) -> Any:
        """
          Récupère le plus grand élement numérique d'une Serie
          :returns: L'élément le plus grand
        """
        if isinstance(self.data, dict):
            return max(list(self.data.values()))
        if isinstance(self.data, list):
            return max(self.data)

    def mean(self) -> Any:
        """
          Calcul de la moyenne des élements d'une Serie
          :returns: La moyenne des éléments
          :raises: ValueError si les éléments ne sont pas numériques
        """

        if isinstance(self.data, dict):
            try:
                return np.mean(list(self.data.values()))
            except Exception as e:
                logging.log(logging.ERROR, f"La moyenne ne peut pas être calculé car : {e}")
        if isinstance(self.data, list):
            try:
                return np.mean(self.data)
            except Exception as e:
                logging.log(logging.ERROR, f"La moyenne ne peut pas être calculé car : {e}")

    def std(self) -> Any:
        """
          Calcul de l'écart-type des élements d'une Serie
          :returns: L'écart-type
          :raises: ValueError si les éléments ne sont pas numériques
        """
        if isinstance(self.data, dict):
            try:
                return np.std(list(self.data.values()))
            except Exception as e:
                logging.log(logging.ERROR, f"L'écart-type ne peut pas être calculé car : {e}")
        if isinstance(self.data, list):
            try:
                return np.std(self.data)
            except Exception as e:
                logging.log(logging.ERROR, f"L'écart-type ne peut pas être calculé car : {e}")


class DataFrame:
    """
        Ensemble de Serie ayant toutes les mêmes listes d'index
    """

    def __init__(self, **kwargs):
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe DataFrame à partir d'un
            ensemble de Series
            :param series: Les séries
        """

        if kwargs.get("colonnes"):
            if not isinstance(kwargs.get("colonnes"), list):
                logging.log(logging.ERROR,
                            f"Type attendu pour le paramètre colonnes : {list}. Type reçu {type(kwargs.get('colonnes'))} ")
            else:
                self.colonnes = kwargs.get("colonnes")
        if kwargs.get("data"):
            self.data = kwargs.get("data")

        if kwargs.get("colonnes") and kwargs.get("data"):
            self.data = list(self.data)

        elif kwargs.get("series"):
            series = kwargs.get("series")
            if series:
                self.colonnes = [serie.name if serie.name is not None else f"Unnamed {index}" for (index, serie) in
                                 enumerate(series)]

                self.data = [serie.data for serie in series]

    @property
    def iloc(self):
        """
            Propriété de la classe DataFrame permettant une indexation basée sur la position des éléments
            :return:
        """
        # logging.exception("NotImplementedError")
        raise NotImplementedError

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une DataFrame
          :returns: Le nombre d'éléments le plus grand
        """
        return len(self.data)

    def min(self) -> Any:
        """
            Récupère le plus petit élement numérique d'une DataFrame
            :returns: L'élement le plus petit pour chaque colonne
        """
        # print(self.data)

        minimums = [np.min(element) for element in self.data]
        return minimums

    def max(self) -> Any:
        """
            Récupère le plus grand élement numérique d'une DataFrame
            :returns: L'élement le plus grand pour chaque colonne
        """
        maximums = [np.max(element) for element in self.data]
        return maximums

    def mean(self):
        """
          Calcul de la moyenne de l'ensemble des colonnes d'une dataframe
          :returns: La moyenne des éléments de chaque colonne
          :raises: ValueError si les éléments ne sont pas numériques
        """
        moyennes = [np.mean(element) for element in self.data]
        return moyennes

    def std(self):
        """
          Calcul de l'écart-type des élements d'une DataFrame
          :returns: L'écart-type de chaque colonne numérique
          :raises: ValueError si une colonne n'est pas numérique
        """
        stds = [np.std(element) for element in self.data]
        return stds

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]):
        """
            Permet de combiner et d'agréger plusieurs lignes d'un DataFrame en formant des groupes à partir d'une
            ou plusieurs colonnes.
            :param by: Le nom de la ou des colonnes sur lesquelles grouper
            :param agg: La stratégie d'agrégation des colonnes
            :return: Le nouvel objet DataFrame ayant été regroupé
        """

        is_in_list = [True if element in self.colonnes else False for element in by]

        if False in is_in_list:
            raise ValueError
        else:
            p = []
            for i in range(len(by)):
                p.append(agg.get(by[i])(self.data[self.colonnes.index(by[i])]))
            # self.data[self.colonnes.index(by[0])]
            return p
        # raise NotImplementedError

    def join(self, other, left_on: List[str] | str, right_on: List[str] | str, how: str = "left"):
        """
           Permet de combiner des données provenant de deux DataFrames
              :param other: L'autre DataFrame
              :param left_on: Le nom de la ou des colonnes de la dataframe de gauche (``self``)
              :param right_on: Le nom de la ou des colonnes de la dataframe de droite (``other``)
              :param how: La manière dont la jointure sera faite (``à gauche, à droite, intérieures et pleines``)
              :return: Le nouvel objet DataFrame ayant été combiné avec une l'autre dataframe
        """
        if not isinstance(other, DataFrame):
            logging.log(logging.CRITICAL, f"Type attendu pour other : {DataFrame}. Got {type(other)}")
        how_list = ["left", "right", "inner", "outer"]
        if not isinstance(left_on, list) or isinstance(right_on, list):
            logging.log(logging.CRITICAL, "Argument left_on ou right_on non conformes")
        if how not in how_list:
            logging.log(logging.CRITICAL, f"Argument attendu pour how : {' ou '.join(how_list)}. Got {type(other)}")

        raise NotImplementedError

    def __repr__(self):
        """
            Permet de représenter l'instance d'une DataFRame de manière plus lisisble pour l'utilisateur
            :param self: L'instance par laquelle la méthode est appelé
            :return: La chaîne de caractère représentant l'objet self
        """
        p = '\t'.join(self.colonnes)
        for row in list(map(list, zip(*self.data))):
            p += "\n"
            for element in row:
                p += str(element) + "\t"
        return f"{p} \n"


def read_csv(path: str, delimiter: str = ","):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")

    try:
        with open(path, mode="r") as f:
            reader = csv.reader(f, delimiter=delimiter)
            p = [f"{delimiter}".join(row).split(delimiter) for row in reader]
            columns = p[0]
            p = list(map(list, zip(*p[1:])))
            dataframe = DataFrame(colonnes=columns, data=p)
    except Exception as e:
        raise FileExistsError(f"File Loading error because of {e}")
    else:
        return dataframe


# Todo : Gérer le paramètre orient pour la lecture du fichier
def read_json(path: str, orient: str = "records"):
    if orient != "records" and orient != "columns":
        raise TypeError(f"Unexpected value for keyword argument : {orient}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")

    try:
        with open(path, mode="r") as f:
            json_object = json.load(f)
            if orient == "records":
                json_dataframe = DataFrame(
                    data=[[obj[key] for obj in json_object] for key in list(json_object[0].keys())],
                    colonnes=list(json_object[0].keys()))
            if orient == "columns":
                json_dataframe = DataFrame(
                    data=[list(v.values()) for v in json_object.values()],
                    colonnes=list(json_object.keys()))
    except Exception as exc:
        raise Exception(f"Another exception occured because {exc}")
    else:
        return json_dataframe
