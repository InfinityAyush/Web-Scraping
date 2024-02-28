
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

df = pd.read_csv("Input.csv")

num = len(df)
for i in range(num):
    a = df["URL_ID"].iloc[i]
    b = df["URL"].iloc[i]
    b = str(b)

    req = requests.get(b)

    soup = BeautifulSoup(req.content, "html.parser")
    articles = soup.find_all('article')

    # Check if there are any articles
    if articles:
        title = articles[0].text
        final_txt = articles[0].text
        final_txt = title + final_txt[:-82]

        a = str(int(a)) + '.txt'
        file_path = os.path.join("Data", a)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(final_txt)
    else:
        print(f"No articles found for URL_ID: {a}")
