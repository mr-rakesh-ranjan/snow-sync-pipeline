import pandas as pd 
from bs4 import BeautifulSoup
import re 

from bs4 import BeautifulSoup
def fabricate_csv(df : 'pd.core.frame.DataFrame'):
    
    # print(df["number"][0])
    for i in range(0, len(df), 1):
        df['text'][i] = BeautifulSoup(df['text'][i], "lxml").text
        df['text'][i] = re.sub(r'\s', ' ', df['text'][i])
    df.to_csv("serviceNow_cleaned.csv", index=False)
    return df
    
    

df1 = pd.read_csv("./kb_articles.csv", encoding='unicode_escape')
new_csv = fabricate_csv(df=df1)
new_csv.to_csv("serviceNow_cleaned.csv", index=False)