import mybear as mb
import pandas as pd

if __name__ == "__main__":
    df1 = mb.read_csv("articles.csv")
    df2 = mb.read_json("articles.json")
    pd_df1 = pd.read_csv("articles.csv")
    pd_df2 = pd.read_json("articles.json")
    print(df1.join(df2, left_on="name", right_on="price", how="left"))
    serie1 = mb.Series(data=[1,2,3,4,5], name="a")
    for element in serie1:
        print(element)


    #print(pd_df1.merge(pd_df2, how="left", left_on="name", right_on="price"))
