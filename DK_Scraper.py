import pandas as pd
import utils
import io

BASE_URL = 'hhtp://rotoguru1.com/cgi-bin/fyday.pl?game=dk&csv=1&week=WEEK&year=YEAR'
WEEKS=list(map(str,range(1,18)))
YEARS=list(map(str,range(2014,2021)))

all_games=pd.DataFrame()
for yr in YEARS:
    for wk in WEEKS:
        soup=utils.soup(BASE_URL.replace("WEEK", wk).replace("YEAR",yr))
        all_games=pd.concat([all_games,pd.read_csv(io.STRINGIO(soup.find('pre').text),sep=';')])
all_games