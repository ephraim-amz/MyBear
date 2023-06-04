import mybear as mb
import pandas as pd

if __name__ == "__main__":
    my_dict = {'col1': [1, 2, 3], 'col2': [ord('a'), ord('b'), ord('c')], 'col3': [0, 1, 0]}
    first_serie = mb.Series(data=list(range(4)), name='a')
    second_serie = mb.Series(list(range(4)), name='b')

    pdf1 = pd.read_csv("articles.csv")
    pdf2 = pd.read_json("articles.json")

    df1 = mb.read_csv("articles.csv")
    df2 = mb.read_json("articles.json")

    # print(df)
    # print(type(df.iloc[0, 2]))

    df_m = mb.DataFrame(series=[first_serie, second_serie])

    # print(df_m.iloc[0:2, 0:2])

    # print(df.groupby("name").sum())
    # df_mb = mb.DataFrame(colonnes=['a', 'b'], data=[[1, 3], [2, 4]])

    # df_json = mb.read_json("oriented_records.json", orient="records")

    # df_1 = pd.read_csv("articles.csv") # Good
    # df_2 = mb.read_csv("articles.csv")
    # df_3 = df_1.join(other=df_2, on="")
    # df_2.data[1] = [float(df_2.data[1][i]) for i in range(len(df_2.data[1]))]
    # print(df_2.groupby(["name"], agg={"name": np.sum}))
    # print(df_1.groupby(by=["name"]).min())
    pdf2['date'] = pdf2['date'].astype(str)
    # print(pdf1.merge(right=pdf2, left_on=["name", "date"], right_on=["date", "price"], how="left"))

    # print(df1.join(right_dataframe=df2, left_on="name", right_on="date"))
    print(df1.join(other=df2, left_on="name", right_on="date", how="right"))
    # print(df.mean())
    # df = pd.read_csv("articles.csv")
    # print(first_serie.iloc(0))
    # print(my_serie.mean(), type(my_serie.mean()))
    # m = my_serie.iloc([1,3])   # print(serie.iloc[1:])
    # df_mb = mb.read_json("notes.json")
    # p4.py = pd.read_json("articles.json", orient="columns")
    # q = pd.read_json("articles.json", orient="records")
    # q.to_json("oriented_columns.json", orient="columns")
    # q.to_json("oriented_records.json", orient="records")
    # print(p4.py)
    # print(q)
    # print(my_serie.mean())
