# MyBear

**MyBear** est une librairie Python de gestion de données alternative à la librairie *pandas* qui est très populaire


## Comment l'installer sur son poste ?

Clone du repo via ssh
```bash
git clone git@github.com:ephraim-amz/MyBear.git
```

Clone du repo via https :
```bash
git clone https://github.com/ephraim-amz/MyBear.git
```

## Comment utiliser le module sur son poste ?

```python
import mybear as mb
```


```python
from mybear import Series, DataFrame, read_csv, read_json
```

## Classe Series


```python
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


    def __set_name(self, name) -> None:
        

    def __getitem__(self, index: Union[List, int]):
        """
            Fonction permettant de d'indexer l'instance d'une classe, nécessaire pour la propriété iloc
            (Fonction non optimale car la notation est object.iloc(index) ou object.iloc([start,stop])
                et non object.iloc[index] object.iloc[start:stop]
            :param index: Index
            :return: Nouvel objet de type Serie indexée
        """
       
    @property
    def iloc(self) -> Any:
        """
            Propriété de la classe Series permettant une indexation basée sur la position des éléments
            :raise: IndexError: Si l'index n'est pas un int ou l'index est invalide
            :return: lambda appelant la fonction __getitem__ définit précédemment
        """

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une Serie
          :returns: Le nombre d'éléments le plus grand
        """

    def min(self) -> Any:
        """
          Récupère le plus petit élement numérique d'une Serie
          :returns: L'élement le plus petit
        """

    def max(self) -> Any:
        """
          Récupère le plus grand élement numérique d'une Serie
          :returns: L'élément le plus grand
        """

    def mean(self) -> Any:
        """
          Calcul de la moyenne des élements d'une Serie
          :returns: La moyenne des éléments
          :raises: ValueError si les éléments ne sont pas numériques
        """


    def std(self) -> Any:
        """
          Calcul de l'écart-type des élements d'une Serie
          :returns: L'écart-type
          :raises: ValueError si les éléments ne sont pas numériques
        """

    def __repr__(self):
        """
            Redéfinition de la méthode __repr__ permettant de formatter l'affichage de l'instance d'une classe Series
            :returns : Une chaîne de caractères correspondant à l'instance de la classe Series
        """

    def __len__(self):
        """
            Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe Series
            :returns : Une chaîne de caractères correspondant à l'instance de la classe Series
        """

```

## Classe DataFrame
```python
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


    @property
    def iloc(self):
        """
            Propriété de la classe DataFrame permettant une indexation basée sur la position des éléments
            :return:
        """

    def count(self) -> Any:
        """
          Récupère le nombre d'élements présent dans une DataFrame
          :returns: Le nombre d'éléments le plus grand
        """

    def min(self) -> Any:
        """
            Récupère le plus petit élement numérique d'une DataFrame
            :returns: L'élement le plus petit pour chaque colonne
        """

    def max(self) -> Any:
        """
            Récupère le plus grand élement numérique d'une DataFrame
            :returns: L'élement le plus grand pour chaque colonne
        """

    def mean(self):
        """
          Calcul de la moyenne de l'ensemble des colonnes d'une dataframe
          :returns: La moyenne des éléments de chaque colonne
          :raises: ValueError si les éléments ne sont pas numériques
        """

    def std(self):
        """
          Calcul de l'écart-type des élements d'une DataFrame
          :returns: L'écart-type de chaque colonne numérique
          :raises: ValueError si une colonne n'est pas numérique
        """

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]):
        """
            Permet de combiner et d'agréger plusieurs lignes d'un DataFrame en formant des groupes à partir d'une
            ou plusieurs colonnes.
            :param by: Le nom de la ou des colonnes sur lesquelles grouper
            :param agg: La stratégie d'agrégation des colonnes
            :return: Le nouvel objet DataFrame ayant été regroupé
        """


    def join(self, other, left_on: List[str] | str, right_on: List[str] | str, how: str = "left"):
        """
           Permet de combiner des données provenant de deux DataFrames
              :param other: L'autre DataFrame
              :param left_on: Le nom de la ou des colonnes de la dataframe de gauche (``self``)
              :param right_on: Le nom de la ou des colonnes de la dataframe de droite (``other``)
              :param how: La manière dont la jointure sera faite (``à gauche, à droite, intérieures et pleines``)
              :return: Le nouvel objet DataFrame ayant été combiné avec une l'autre dataframe
        """

    def __repr__(self):
        """
            Redéfinition de la méthode __repr__ permettant de formatter l'affichage de l'instance d'une classe DataFrame
            :returns : Une chaîne de caractères correspondant à l'instance de la classe DataFrame
        """

    def __len__(self):
        """
            Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe DataFrame
            :returns : Une chaîne de caractères correspondant à l'instance de la classe DataFrame
        """
```

## Fonctions read_csv et read_json

```python
def read_csv(path: str, delimiter: str = ","):
    """
        Fonction permettant de créer une nouvelle instance de la classe DataFrame à partir d'un fichier csv
        :param path: Le chemin relatif, absolu, ou tout simplement le nom du fichier csv
        :param delimiter: Le séparateur d'éléments au sein du fichier (par défaut une virgule)
        :returns : Une nouvelle instance de la classe DataFrame à partir des données du fichier
    """


def read_json(path: str, orient: str = "records"):
    """
          Fonction permettant de créer une nouvelle instance de la classe DataFrame à partir d'un fichier JSON
          :param path: Le chemin relatif, absolu, ou tout simplement le nom du fichier csv
          :param orient: L'orientation du fichier JSON (records par défaut)
          :returns : Une nouvelle instance de la classe DataFrame à partir des données du fichier
      """
```