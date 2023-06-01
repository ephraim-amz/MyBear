import logging
from typing import Any
from typing import List
from typing import Union

import numpy as np

logging.basicConfig(level=logging.INFO)


class Series:
    """
    Colonne dans un DataFrame qui contient en plus des données,
    une étiquette (un nom), et des informations statistiques déjà
    présentes et calculées automatiquement lors de la création de
    la Serie (taille, nombre de valeurs manquantes et type de données)
    """

    def __init__(self, data: Union[range, List[Any]], name: str = None) -> None:
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

    def __eq__(self, other) -> bool:
        """
        Redéfinition de la méthode __eq__ permettant de comparer deux instances de la classe Serie

        Returns
        -------
        bool
            True or False
        """
        return self.data == other.data and self.name == other.name
