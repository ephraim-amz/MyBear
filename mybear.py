import numpy as np
import json
import logging
import csv
import os
import copy
from typing import List, Any, Union, Dict, Callable, Tuple

logging.basicConfig(level=logging.INFO)


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

    def __set_name(self, name: str) -> None:
        """
            Setter permettant de définir l'attribut name de la classe Series
            :param name: Le futur nom de l'instance Series
            :return: Nouvel objet de type Serie indexée
        """
        self.name = name

    def __getitem__(self, index: Union[slice, int]):
        """
            Fonction permettant de d'indexer l'instance d'une classe, nécessaire pour la propriété iloc
            (Fonction non optimale car la notation est object.iloc(index) ou object.iloc([start,stop])
                et non object.iloc[index] object.iloc[start:stop]
            :param index: Index
            :return: Nouvel objet de type Serie indexée
        """
        if isinstance(index, int):
            return self.data[index]
        elif isinstance(index, slice):
            return Series(data=self.data[index], name=self.name if self.name is not None else "Undefined")
        else:
            logging.log(logging.ERROR, f"Type attendu : {slice} ou {int}. Reçu : {type(index)}")

    @property
    def iloc(self) -> Any:
        """
            Propriété de la classe Series permettant une indexation basée sur la position des éléments
            :raise: IndexError: Si l'index n'est pas un int ou l'index est invalide
            :return: lambda appelant la fonction __getitem__ définit précédemment
        """
        return self

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

    def __str__(self):
        """
            Redéfinition de la méthode __str__ permettant de formatter l'affichage de l'instance d'une classe Series
            :returns : Une chaîne de caractères correspondant à l'instance de la classe Series
        """
        str_builder = ["{}\t{}".format(i, val) for i, val in enumerate(self.data)]
        str_builder.append(f"Name: {self.name}, dtype: {type(self.data[0])}")
        return "\n".join(str_builder)

    def __len__(self):
        """
            Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe Series
            :returns : Une chaîne de caractères correspondant à l'instance de la classe Series
        """
        return self.count()


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
                            f"Type attendu pour le paramètre colonnes : {list}. "
                            f"Type reçu {type(kwargs.get('colonnes'))} ")
            else:
                self.colonnes = kwargs.get("colonnes")

        if kwargs.get("colonnes") and kwargs.get("data"):
            self.data = {colonne: Series(data=serie, name=colonne) for colonne, serie in
                         zip(self.colonnes, kwargs.get("data"))}

        elif kwargs.get("series"):
            series_list = kwargs.get("series")
            if series_list:
                self.colonnes = [serie.name if serie.name is not None else f"Unnamed {index}" for (index, serie) in
                                 enumerate(series_list)]

                self.data = {colonne: serie for colonne, serie in zip(self.colonnes, series_list)}

    def __getitem__(self, index: Tuple[Union[int, slice], Union[int, slice]]):
        if not isinstance(index, tuple):
            logging.exception(f"Type d'index attendu : {tuple}. Type reçu : {type(index)}")
            raise IndexError
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
            return Series(data=list(self.data.values())[column_start].data[row_start:row_stop],
                          name=list(self.data.keys())[column_start])
        elif is_integer_and_slice:
            data = [d.data[row_start] for d in self.data.values()]
            columns = self.colonnes[column_start:column_stop]
            series = [Series(data=[val], name=name) for val, name in zip(data, columns)]
            return DataFrame(series=series)
        elif is_slice_and_slice:
            data = [d.data[row_start:row_stop] for d in self.data.values()]
            columns = self.colonnes[column_start:column_stop]
            series = [Series(data=[series_data] if not isinstance(series_data, list) else series_data, name=series_name)
                      for series_data, series_name in zip(data, columns)]
            return DataFrame(series=series)

    @property
    def iloc(self):
        """
            Propriété de la classe DataFrame permettant une indexation basée sur la position des éléments
            :return:
        """
        return self

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une DataFrame
          :returns: Le nombre d'éléments le plus grand
        """
        return self.data.get(list(self.data.keys())[0]).count()

    def min(self) -> Any:
        """
            Récupère le plus petit élement numérique d'une DataFrame
            :returns: L'élement le plus petit pour chaque colonne
        """

        minimums = [Series(data=[element.min()], name=name) for name, element in self.data.items()]
        return DataFrame(series=minimums)

    def max(self) -> Any:
        """
            Récupère le plus grand élement numérique d'une DataFrame
            :returns: L'élement le plus grand pour chaque colonne
        """
        maximums = [Series(data=[element.max()], name=name) for name, element in self.data.items()]
        return DataFrame(series=maximums)

    def mean(self):
        """
          Calcul de la moyenne de l'ensemble des colonnes d'une dataframe
          :returns: La moyenne des éléments de chaque colonne
          :raises: ValueError si les éléments ne sont pas numériques
        """
        moyennes = [Series(data=[element.mean()], name=name) for name, element in self.data.items()]
        return DataFrame(series=moyennes)

    def std(self):
        """
          Calcul de l'écart-type des élements d'une DataFrame
          :returns: L'écart-type de chaque colonne numérique
          :raises: ValueError si une colonne n'est pas numérique
        """
        stds = [Series(data=[element.std()], name=name) for name, element in self.data.items()]
        return DataFrame(series=stds)

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]):
        """
            Permet de combiner et d'agréger plusieurs lignes d'un DataFrame en formant des groupes à partir d'une
            ou plusieurs colonnes.
            :param by: Le nom de la ou des colonnes sur lesquelles grouper
            :param agg: La stratégie d'agrégation des colonnes
            :return: Le nouvel objet DataFrame ayant été regroupé
        """

        if not isinstance(by, (list, str)):
            raise Exception

        is_in_list = [True if element in self.colonnes else False for element in by]

        if False in is_in_list:
            raise ValueError
        else:
            # Pour chaque colonne, regarder les valeurs uniques de la colonne sélectionné lors du by

            # p4.py = [self.data[self.colonnes.index(by[i])] for i in range(len(by))] Lorsque by aura plusieurs colonnes
            # unique_cols = list(set(self.data[self.colonnes.index(by[0])]))
            new_serie = Series(data=[], name=by[0])
            for val in self.data.get(by[0]).data:
                if val not in new_serie.data:
                    new_serie.data.append(val)
            print()
            # TODO : Retourner une exception si la fonction d'aggrégation n'est pas possible pour la fonction appelé
            # TODO : Effectuer la fonction d'aggrégation pour chaque colonne

            # TODO : Créer un nouveau dataframe à partir de chaque nouvelle colonne
            # TODO : Retourner cet instance nouvellement créée
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
        if not isinstance(left_on, (list, str)) and not isinstance(right_on, (list, str)):
            logging.log(logging.CRITICAL, "Argument left_on ou right_on non conformes")
        if how not in how_list:
            logging.log(logging.CRITICAL, f"Argument attendu pour how : {' ou '.join(how_list)}. Got {type(other)}")

        result = []
        df_join = None

        if isinstance(left_on, str):
            left_on = [left_on]
        if isinstance(right_on, str):
            right_on = [right_on]

        if how == "left":
            left_dataframe = copy.deepcopy(self)
            left_dataframe.colonnes = [''.join([colonne, "_x"]) if colonne in right_on else colonne for colonne in
                                       left_dataframe.colonnes]
            for element in left_dataframe.data.get(left_on[0]):
                if element in other.data.get(right_on[0]).data:
                    left_dataframe.colonnes.append("price_y")
                    left_dataframe.colonnes.append(other.data.get("price")[0])
                    left_dataframe.colonnes.append(other.data.get("date")[0])
                    #left_dataframe.colonnes = ["price", other.data.get("price")[0]]
                    left_dataframe.data.update()




            """
            for entry_self in self.data.values():
                entry_result = entry_self
                matching_entries = []

                for entry_other in other.data.values():
                    matching = True

                    # Gestion de taille à faire

                    for left_key, right_key in zip(left_on, right_on):
                        left_serie_values = self.iloc[:, self.colonnes.index(left_key)].data
                        right_serie_values = other.iloc[:, other.colonnes.index(right_key)].data

                        if left_serie_values != right_serie_values:
                            matching = False
                            break

                    if matching:
                        # self.data.update({right_key: other.iloc[:, other.colonnes.index(right_key)]})
                        matching_entries.append(entry_other)

                if len(matching_entries) > 0:
                    entry_result['matching_entries'] = matching_entries
                else:
                    entry_result['matching_entries'] = []

                result.append(entry_result)

            self_data = [list(entry.values()) for entry in self.data]
            other_data = [list(entry.values()) for entry in other.data]
            df_join = DataFrame(data=self_data + other_data)
            
            return df_join
            """
        elif how == "right":
            ...
        elif how == "inner":
            ...
        elif how == "outer":
            ...

        return df_join

    def __str__(self):
        """
            Redéfinition de la méthode __str__ permettant de formatter l'affichage de l'instance d'une classe DataFrame
            :returns : Une chaîne de caractères correspondant à l'instance de la classe DataFrame
        """
        data = [d.data for d in self.data.values()]
        p = "\t".join(self.colonnes)
        for index, element in enumerate(zip(*data)):
            p += "\n"
            p += str(index) + " " + '   '.join(str(item).ljust(len(self.colonnes)) for item in element)
        return p

    def __len__(self):
        """
            Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe DataFrame
            :returns : Une chaîne de caractères correspondant à l'instance de la classe DataFrame
        """
        return self.count()


def read_csv(path: str, delimiter: str = ","):
    """
        Fonction permettant de créer une nouvelle instance de la classe DataFrame à partir d'un fichier csv
        :param path: Le chemin relatif, absolu, ou tout simplement le nom du fichier csv
        :param delimiter: Le séparateur d'éléments au sein du fichier (par défaut une virgule)
        :returns : Une nouvelle instance de la classe DataFrame à partir des données du fichier
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")

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
                    if element[0] == '-' and element[1:].isdigit():
                        line[index] = -int(element[1:])
                    elif '.' in element and element[element.index(".") + 1:].isnumeric():
                        try:
                            line[index] = float(element)
                        except ValueError:
                            logging.log(logging.CRITICAL, "Value can not be converted to float")

            dataframe = DataFrame(colonnes=columns, data=lines)
    except Exception as e:
        raise FileExistsError(f"File Loading error because of {e}")
    else:
        return dataframe


def read_json(path: str, orient: str = "records"):
    """
          Fonction permettant de créer une nouvelle instance de la classe DataFrame à partir d'un fichier JSON
          :param path: Le chemin relatif, absolu, ou tout simplement le nom du fichier csv
          :param orient: L'orientation du fichier JSON (records par défaut)
          :returns : Une nouvelle instance de la classe DataFrame à partir des données du fichier
      """
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
