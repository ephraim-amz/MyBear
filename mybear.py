import numpy as np
import json
import logging
import csv
import os
from typing import List, Dict, Callable, Any, Union


class Series:
    """
        Colonne dans un DataFrame qui contient en plus des données, une étiquette (un nom),
        et des informations statistiques déjà présentes et calculées automatiquement
        lors de la création de la Serie (taille, nombre de valeurs manquantes et type de données)
    """

    def __init__(self, data: Union[dict, range, List[Union[Any]]], name: str = None):
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

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une Serie
          :returns: Le nombre d'éléments le plus grand
        """
        return len(self.data)

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

    def __repr__(self) -> str:
        """
            Permet de représenter l'instance d'une Serie de manière plus lisisble pour l'utilisateur
        """
        if isinstance(self.data, dict):
            p = "\n".join([f"{k}\t{v}" for k, v in self.data.items()])
            return f"{p}\nName: {self.name}, dtype: {type(list(self.data.values())[0])}"
        else:
            p = "\n".join([f"{index}\t{value}" for (index, value) in zip(self.index, self.data)])
            return f"{p}\nName: {self.name}, dtype: {type(self.data[0])}"


class DataFrame:
    def __init__(self, series: Union[Series]):
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe DataFrame
            :param series: Les séries
        """

    @property
    def iloc(self):
        """
            Propriété de la classe DataFrame permettant une indexation basée sur la position des éléments
            :return:
        """
        # logging.exception("NotImplementedError")
        raise NotImplementedError

    def max(self) -> Any:
        """
                  Récupère le plus grand élement numérique d'une Serie
                """
        raise NotImplementedError

    def min(self) -> Any:
        """
                  Récupère le plus petit élement numérique d'une Serie
                """
        raise NotImplementedError

    def mean(self) -> np.float64:
        raise NotImplementedError

    def std(self) -> np.float64:
        raise NotImplementedError

    def count(self) -> np.int64:
        """
                  Récupère le nombre d'élements présent dans une Serie
                """
        raise NotImplementedError

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]):
        raise NotImplementedError

    def join(self, other, left_on: List[str] | str, right_on: List[str] | str, how: str = "left"):
        raise NotImplementedError

    def __repr__(self):
        # TODO : Change function
        p = '    '.join(self.columns) + "\n"
        p += "\n".join([f"{'    '.join(row)}" for row in self.data])
        return f"{p}\n{self.dtype}"


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
