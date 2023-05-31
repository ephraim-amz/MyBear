import mybear as mb
import pandas as pd


if __name__ == "__main__":
    df1 = mb.read_csv("articles.csv")
    df2 = mb.read_json("articles.json")
    print(df1.join(df2, how="left", left_on="name", right_on="name"))

