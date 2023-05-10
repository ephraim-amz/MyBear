import numpy as np
import json
import logging
import csv
import os
from typing import List, Dict, Callable, Any, Union, overload


class Series:
    """
        Colonne dans un DataFrame qui contient en plus des données, une étiquette (un nom),
        et des informations statistiques déjà présentes et calculées automatiquement
        lors de la création de la Serie (taille, nombre de valeurs manquantes et type de données)
    """

    def __init__(self, data: Union[dict, range, List[Union[Any]]], name: str = None) -> None:
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe Series
            :param data: Les données qui peuvent être un dictionnaire, un range ou bien une liste d'élements de type divers
            :param name: Le nom qui sera attribué à la série (Valeur None par défaut)
            :return: Nouvel objet de type Serie
        """
        if isinstance(data, range) or isinstance(data, list):
            self.data = list(data)
            self.index = range(len(data))
        elif isinstance(data, dict):
            self.data = data
            self.index = range(len(data.keys()))
        self.name = name

    def set_name(self, name) -> None:
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
        if not isinstance(index, int) or not is_integer_list_with_two_elements:
            logging.log(logging.CRITICAL,
                        f"L'argument passé en paramètre est incorrect.\nType attendu : {list} ou {int}. Type reçu : {type(index)}")
            raise ValueError
        else:
            if isinstance(self.data, dict):
                if isinstance(index, int):
                    return Series({self.index[index]: list(self.data.values())[index]})
                else:
                    data = {list(self.data.keys())[k]: list(self.data.values())[k] for k in range(index[0], index[1])}
                    return Series(data)
            elif isinstance(self.data, list):
                if isinstance(index, int):
                    return Series({self.index[index]: self.data[index]})
                else:
                    return Series(self.data[index[0]: index[1]])

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

    def __repr__(self) -> str:
        """
            Permet de représenter l'instance d'une Serie de manière plus lisisble pour l'utilisateur
            :param self: L'instance par laquelle la méthode est appelé
            :return: La chaîne de caractère représentant l'objet self
        """
        if isinstance(self.data, dict):
            p = "\n".join([f"{k}\t{v}" for k, v in self.data.items()])
            return f"{p}\nName: {self.name}, dtype: {type(list(self.data.values())[0])}"
        else:
            p = "\n".join([f"{index}\t{value}" for (index, value) in zip(self.index, self.data)])
            return f"{p}\nName: {self.name}, dtype: {type(self.data[0])}"


class DataFrame:
    """
        Ensemble de Serie ayant toutes les mêmes listes d'index
    """

    def __init__(self, *series: Series):
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe DataFrame à partir d'un ensemble de Series
            :param series: Les séries
        """
        self.colonnes = [serie.name if serie.name is not None else f"Unnamed {index}" for (index, serie) in
                         enumerate(series)]

        self.data = list(map(list, zip(*[list(serie.data.values()) for serie in series])))

    def __init__(self, colonnes, data):
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe DataFrame à partir des colonnes et des données
            :param colonnes: Les colonnes
            :param data: Liste contenant une liste de liste d'élements même taille
        """
        self.colonnes = colonnes
        self.data = list(map(list, zip(*data)))

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
        raise NotImplementedError

    def join(self, other, left_on: List[str] | str, right_on: List[str] | str, how: str = "left"):
        """
           Permet de combiner des données provenant de deux DataFrames
              :param other: L'autre DataFrame
              :param left_on: Le nom de la ou des colonnes de la dataframe de gauche (``self``)
              :param right_on: Le nom de la ou des colonnes de la dataframe de droite (``other``)
              :param how: La manière dont la jointure sera faite (``à gauche, à droite, intérieures et pleines``)
              :return: Le nouvel objet DataFrame ayant été combiné avec une l'autre dataframe
        """
        raise NotImplementedError

    def __repr__(self):
        """
            Permet de représenter l'instance d'une DataFRame de manière plus lisisble pour l'utilisateur
            :param self: L'instance par laquelle la méthode est appelé
            :return: La chaîne de caractère représentant l'objet self
        """
        p = '\t'.join(self.colonnes)
        for row in self.data:
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
            p = [",".join(row) for row in reader]
            dataframe = DataFrame(data=p[1:], columns=p[0], dtype=object, delimiter=delimiter)
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
            json_dataframe = DataFrame(data=json_object, columns=list(json_object[0].keys()))
    except Exception as excp:
        raise Exception(f"Another exception occured because {excp}")
    else:
        return json_dataframe
