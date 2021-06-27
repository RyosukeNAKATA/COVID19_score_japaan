import requests
import re

from IPython.core.display import display
import pandas as pd
from numpy import index_exp
import subprocess as sp


def main():
    sp.call("wget https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv", shell=True)
    sp.call("cat nhk_news_covid19_prefectures_daily_data.csv|sed '2,$s/,-/,/g' >new", shell=True)
    sp.call("mv new nhk_news_covid19_prefectures_daily_data.csv", shell=True)
    df = pd.read_csv("nhk_news_covid19_prefectures_daily_data.csv")
    sp.call("rm nhk_news_covid19_prefectures_daily_data.csv", shell=True)
    sp.call("wget https://github.com/ytakefuji/covid_score_japan/raw/main/jppop.xlsx", shell=True)
    populations = pd.read_excel("jppop.xlsx", header=0)
    sp.call("rm jppop.xlsx", shell=True)

    populations = populations[1:-3]
    population = populations.iloc[:, 33].reset_index()
    date = df.iloc[-1]['日付']
    df = df[df['日付']==date].reset_index()
    prefecture = df.iloc[:, 3]
    data = pd.DataFrame({
        "prefecture": prefecture,
        "death": range(len(prefecture)),
        "population": range(len(prefecture)),
        "score": range(len(prefecture)),
    })
    data = data.astype({"score": 'float64'})

    for i in range(len(prefecture)):
        data.at[data.index[i], 'prefecture'] = prefecture[i]
        data.at[data.index[i], 'death'] = int(df.loc[df['都道府県名']==prefecture[i], '各地の死者数_累計'])
        data.at[data.index[i], 'population'] = int(population.iloc[i, 1])
        data.at[data.index[i], 'score'] = data.at[data.index[i], 'death']/data.at[data.index[i], 'population']
        data = data.sort_values(by=['score'])
    display(data)


if __name__ == "__main__":
    main()
