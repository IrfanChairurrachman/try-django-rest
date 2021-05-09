import csv
from collections import OrderedDict
import pandas as pd

from django.urls import path, include

def get_wisata():
    wisata = []
    with open('snippets/dataset.csv','r') as f:
        r = csv.DictReader(f)
        for row in r:
            print(row)
            wisata.append(row)
        # od = collections.OrderedDict(r)
    return wisata


def get_popular():
    metadata = pd.read_csv('snippets/dataset.csv', low_memory=False)
    # Calculate mean of vote average column
    C = metadata['vote_average'].mean()
    # Calculate the minimum number of votes required to be in the chart, m
    m = metadata['vote_count'].quantile(0)

    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)
    
    filtered = metadata.copy().loc[metadata['vote_count'] >= m]

    filtered['score'] = filtered.apply(weighted_rating, axis=1)

    #Sort movies based on score calculated above
    filtered = filtered.sort_values('score', ascending=False)

    df_baru = filtered.to_dict('records', into=OrderedDict)
    
    # return filtered
    return df_baru

# df = get_popular()
# df_baru = df.to_dict(into=OrderedDict)
# print(type(df))
# # print(df_baru)