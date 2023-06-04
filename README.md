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
import mybear
```

```python
from mybear import DataFrame, Series, read_csv, read_json
```

## Classe Series


```python
class Series:
    """
        Colonne dans un DataFrame qui contient en plus des données, une étiquette (un nom),
        et des informations statistiques déjà présentes et calculées automatiquement
        lors de la création de la Serie (taille, nombre de valeurs manquantes et type de données)
    """

    def __init__(self, data: Union[range, List[Any]],
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


    def __getitem__(self, index: Union[List, int]):
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

    @property
    def iloc(self) -> Any:
        """
        Propriété de la classe Series permettant une indexation basée sur la position des éléments

        Returns
        -------
        Series
            L'instance par laquelle la méthode est appelée
        """

    def count(self) -> Any:
        """
        Récupère le nombre d'élements présent dans une Serie

        Returns
        -------
        int
            Le nombre d'éléments de la serie
        """

    def min(self) -> Any:
        """
        Récupère le plus petit élément présent dans une Serie

        Returns
        -------
        int
            L'élement le plus petit
        """

    def max(self) -> Any:
        """
        Récupère le plus grand élément présent dans une Serie

        Returns
        -------
        int
            L'élement le plus grand
        """

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

    def __str__(self):
        """
        Redéfinition de la méthode __str__ permettant de formatter l'affichage de l'instance d'une classe Series

        Returns
        -------
        str
            Une chaîne de caractères correspondant à l'instance de la classe Series
        """

    def __len__(self):
        """
        Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe Series

        Returns
        -------
        int
            Le nombre d'élements
        """

    def __eq__(self, other) -> bool:
    """
        Redéfinition de la méthode __eq__ permettant de comparer deux instances de la classe Serie

        Returns
        -------
        bool
            True or False
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


    @property
    def iloc(self):
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

    def count(self) -> Any:
        """
        Récupère le nombre d'élements présent dans une Serie

        Returns
        -------
        int
            Le nombre d'éléments du DataFrame
        """

    def min(self) -> Any:
        """
        Récupère le plus petit élement numérique de chaque Serie composant
        un DataFrame

        Returns
        -------
        DataFrame
            L'élement le plus petit pour chaque colonne
        """

    def max(self) -> Any:
        """
        Récupère le plus grand élement numérique de chaque Serie composant
        un DataFrame

        Returns
        -------
        DataFrame
            L'élement le plus grand pour chaque colonne
        """

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


    def join(
        self,
        other,
        left_on: List[str] | str,
        right_on: List[str] | str,
        how: str = "left"
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

    def __str__(self):
        """
        Redéfinition de la méthode __str__ permettant de formatter l'affichage de l'instance d'une classe DataFrame

        Returns
        -------
        str
            Une chaîne de caractères correspondant à l'instance de la classe DataFrame
        """

    def __len__(self):
        """
        Redéfinition de la méthode __len__ permettant d'utiliser len() pour une instance de la classe DataFrame

        Returns
        -------
        int
            Le nombre d'élements
        """

    def __eq__(self, other):
        """
        Redéfinition de la méthode __eq__ permettant de comparer deux instances de la classe DataFrame

        Returns
        -------
        bool
            True or False
        """
```

## Fonctions read_csv et read_json

```python
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
```
