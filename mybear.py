import csv
import json
import logging
import os

from src.dataframe import DataFrame
from src.series import Series

logging.basicConfig(level=logging.INFO)

Series = Series
DataFrame = DataFrame


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
    if not os.path.exists(os.path.join(path)):
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
                        "." in element and element[element.index(".") + 1 :].isnumeric()
                    ):
                        try:
                            line[index] = float(element)
                        except ValueError as ve:
                            logging.exception("Value can not be converted to float")
                            raise ve
                    # elif re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", element):
                    # line[index] = datetime.strptime(element, "%d-%m-%Y").date()

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
