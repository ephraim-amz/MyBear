import numpy as np
from typing import List, Dict, Callable, Any
import json
import logging
import csv
import os
import numpy as np


class Series:
    def __init__(self, data, **kwargs):
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe Series
            :param data:
            :param kwargs:
        """
        index = kwargs.get("index")
        dtype = kwargs.get("dtype")
        columns = kwargs.get("columns")
        self.index = index
        self.data = data
        self.dtype = dtype
        self.columns = columns

    def __getitem__(self, index):
        if isinstance(index, int):
            return Series({self.index[index]: list(self.data.values())[index]}, index=list(self.index[index]))
        else:
            data = {list(self.data.keys())[k]: list(self.data.values())[k] for k in range(index[0], index[1])}
            return Series(data, index=list(self.data.keys())[index[0]: index[1]])

    @property
    def iloc(self) -> Any:
        """
            Propriété de la classe Series permettant une indexation basée sur la position des éléments
            :return:
        """
        return lambda index: self[index]

    def min(self) -> Any:
        """
          Récupère le plus petit élement numérique d'une Serie
        """
        return min(self.data.values())

    def max(self) -> Any:
        """
          Récupère le plus grand élement numérique d'une Serie
        """
        # Gérer exception valeur non numérique
        return max(self.data.values())

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une Serie
        """
        return len(self.data)

    def std(self) -> Any:
        """
          Calcul de l'écart-type des élements d'une Serie'
        """
        # Gérer exception valeur non numérique
        return np.std(list(self.data.values()))

    def mean(self) -> Any:
        """
          Calcul de la moyenne des élements d'une Serie
        """
        # Gérer exception valeur non numérique
        return np.mean(list(self.data.values()))


    def __repr__(self) -> str:
        """
            Permet de représenter l'instance d'une Serie de manière plus lisisble pour l'utilisateur
        """
        p = "\n".join([f"{k}\t{v}" for k, v in self.data.items()])
        return f"{p}\n{self.dtype}"


class DataFrame:
    def __init__(self, data, **kwargs):
        """
            Fonction __init__ permettant de créer une nouvelle instance de la classe DataFrame
            :param data:
            :param kwargs:
        """
        index = kwargs.get("index")
        columns = kwargs.get("columns")
        dtype = kwargs.get("dtype")
        copy = kwargs.get("copy")
        delimiter = kwargs.get("delimiter")
        self.data = [row.split(delimiter) for row in data]
        self.index = index
        self.columns = columns.split(delimiter)
        self.dtype = dtype
        self.copy = copy

    @property
    def iloc(self):
        """
            Propriété de la classe DataFrame permettant une indexation basée sur la position des éléments
            :return:
        """
        logging.exception("NotImplementedError")
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

    @property
    def columns_(self):
        return self.columns


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
            # p = DataFrame.__new__()
            json_object = json.load(f)
            json_dataframe = DataFrame(data=json_object, columns=list(json_object[0].keys()))
    except Exception as excp:
        raise Exception(f"Another exception occured because {excp}")
    else:
        return json_dataframe
