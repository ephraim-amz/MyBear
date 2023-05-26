import mybear as mb
import pandas as pd
import numpy as np
import logging

if __name__ == "__main__":
    # my_dict = {'col1': [1, 2, 3], 'col2': [ord('a'), ord('b'), ord('c')], 'col3': [0, 1, 0]}
    first_serie = mb.Series([1, 3, 4], name='a')
    second_serie = mb.Series(range(2, 5), name='b')

    # df = pd.DataFrame(my_dict)

    df_m = mb.DataFrame(series=[first_serie, second_serie])
    # df_mb = mb.DataFrame(colonnes=['a', 'b'], data=[[1, 3], [2, 4]])

    # df_json = mb.read_json("oriented_records.json", orient="records")

    df_1 = pd.read_csv("articles.csv") # Good
    df_2 = mb.read_csv("articles.csv")
    # df_3 = df_1.join(other=df_2, on="")
    # df_2.data[1] = [float(df_2.data[1][i]) for i in range(len(df_2.data[1]))]
    print(df_2.groupby(["name"], agg={"name": np.sum}))
    # print(df_1.groupby(by=["name"]).min())
    # print(df_mb.join(other=df_json, left_on="", right_on=""))

    # print(df.mean())
    # df = pd.read_csv("articles.csv")
    # print(first_serie.iloc(0))
    # print(my_serie.mean(), type(my_serie.mean()))
    # m = my_serie.iloc([1,3])   # print(serie.iloc[1:])
    # df_mb = mb.read_json("notes.json")
    # p = pd.read_json("articles.json", orient="columns")
    # q = pd.read_json("articles.json", orient="records")
    # q.to_json("oriented_columns.json", orient="columns")
    # q.to_json("oriented_records.json", orient="records")
    # print(p)
    # print(q)
    # print(my_serie.mean())
