import requests
import pandas as pd

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Query

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():

    url = 'https://pyrebaserealtimedbdemo-7f6cb-default-rtdb.firebaseio.com/ATP.json'
    resp = requests.get(url=url)
    rankingd = resp.json()

    return rankingd


@app.get("/match")
def match(
j1:str = Query(
...,
min_lenght=3, 
max_lenght=50,
title="Player 1 name",
description="Name of the first player"
),
j2:str = Query(
...,
min_lenght=3, 
max_lenght=50,
title="Player 2 name",
description="Name of the second player"
)
):

    url = 'https://pyrebaserealtimedbdemo-7f6cb-default-rtdb.firebaseio.com/ATP.json'
    resp = requests.get(url=url)
    response = resp.json()
    ranking = pd.DataFrame.from_dict(response)
    player1 = ranking[ranking['Player'].str.contains(j1, case=False)]
    player2 = ranking[ranking['Player'].str.contains(j2, case=False)]
    result = {'Player 1': {'name':player1.Player.values[0],'win_percentage':round(player1.Power.values[0]/(player1.Power.values[0]+player2.Power.values[0]),2)},'Player 2': {'name':player2.Player.values[0],'win_percentage':round(player2.Power.values[0]/(player1.Power.values[0]+player2.Power.values[0]),2)}}

    return result