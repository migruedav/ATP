import pandas as pd
import re
from datetime import datetime
import datetime
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Query

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():

    df2021 = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2021.csv')
    df2022 = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2022.csv')

    #df2021.drop(df2021[df2021.winner_rank > 80].index, inplace=True)
    #df2021.drop(df2021[df2021.loser_rank > 80].index, inplace=True)
    #df2022.drop(df2022[df2022.winner_rank > 80].index, inplace=True)
    #df2022.drop(df2022[df2022.loser_rank > 80].index, inplace=True)
    df = pd.concat([df2021, df2022])
    df = df.reset_index()

    datef = []

    for dt in range(len(df['tourney_date'])):
        a = str(df['tourney_date'][dt])
        datef.append(datetime.datetime.strptime(a, '%Y%m%d').strftime('%m/%d/%Y'))

    matches = pd.DataFrame()
    matches['date'] = datef
    matches['tournament'] = df['tourney_name']
    matches['winner'] = df['winner_name']
    matches['loser'] = df['loser_name']
    matches['score'] = df['score']

    winner_games = []
    loser_games = []

    for m in range(len(matches['score'])):
        s = str(matches['score'][m])
        wg = re.findall(r"(\d+)-", s)
        lg = re.findall(r"-(\d+)", s)
        winner_games.append(sum(map(int, wg)))
        loser_games.append(sum(map(int, lg)))

    matches['winner_games'] = winner_games
    matches['loser_games'] = loser_games

    days_diff=[]
    today = datetime.datetime.today()

    for dts in range(len(matches['date'])):
        date_str = date_str = matches['date'][dts]
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        diff = today-datetime_obj
        days_diff.append(diff.days)

    matches['diff of days'] = days_diff

    matches['date_factor'] = (matches['diff of days'] - 547) / (np.min(matches['diff of days']) - 547)
    matches.sort_values(by=['date_factor'],inplace=True)
    matches = matches.reset_index()

    winner_score = []

    for p in range(len(matches['winner_games'])):
        if((matches['winner_games'][p]-matches['loser_games'][p])>0):
            winner_score.append((matches['winner_games'][p]-matches['loser_games'][p])*matches['date_factor'][p])
        else:
            winner_score.append(0)

    matches['winner_score'] = winner_score

    wl = matches['winner'].tolist()
    ll = matches['loser'].tolist()
    all_players = set(wl + ll)
    all_players= sorted(all_players)

    matrix = pd.DataFrame(columns=all_players,index=all_players)

    for p1 in all_players:
        for p2 in all_players:
            matrix.at[p1,p2] = 0

    for i in range(len(matches)):
        matrix.at[matches['winner'][i],matches['loser'][i]] += matches['winner_score'][i]

    a = matrix
    b = np.matmul(a,a)
    c = a+b
    d = c.sum(axis=1)
    d = d.to_dict()

    ranking = pd.DataFrame()
    ranking_player = list(d.keys())
    ranking_power = list(d.values())
    ranking['Player'] = ranking_player
    ranking['Power'] = ranking_power

    ranking.sort_values("Power", ascending=False,inplace=True)
    ranking.Power = ranking.Power.round()
    ranking.reset_index(drop=True, inplace=True)
    ranking.drop(ranking[ranking['Power'] <= 0].index, inplace = True)

    rankingd = ranking.to_html()

    return rankingd



@app.get("/match")
def match(
jugador1:str = Query(
...,
min_lenght=3, 
max_lenght=50,
title="Player 1 name",
description="Name of the first player"
),
jugador2:str = Query(
...,
min_lenght=3, 
max_lenght=50,
title="Player 2 name",
description="Name of the second player"
)
):

    df2021 = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2021.csv')
    df2022 = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2022.csv')
    df = pd.concat([df2021, df2022])
    df = df.reset_index()

    datef = []

    for dt in range(len(df['tourney_date'])):
        a = str(df['tourney_date'][dt])
        datef.append(datetime.datetime.strptime(a, '%Y%m%d').strftime('%m/%d/%Y'))

    matches = pd.DataFrame()
    matches['date'] = datef
    matches['tournament'] = df['tourney_name']
    matches['winner'] = df['winner_name']
    matches['loser'] = df['loser_name']
    matches['score'] = df['score']

    winner_games = []
    loser_games = []

    for m in range(len(matches['score'])):
        s = str(matches['score'][m])
        wg = re.findall(r"(\d+)-", s)
        lg = re.findall(r"-(\d+)", s)
        winner_games.append(sum(map(int, wg)))
        loser_games.append(sum(map(int, lg)))

    matches['winner_games'] = winner_games
    matches['loser_games'] = loser_games

    days_diff=[]
    today = datetime.datetime.today()

    for dts in range(len(matches['date'])):
        date_str = date_str = matches['date'][dts]
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        diff = today-datetime_obj
        days_diff.append(diff.days)

    matches['diff of days'] = days_diff

    matches['date_factor'] = (matches['diff of days'] - 547) / (np.min(matches['diff of days']) - 547)
    matches.sort_values(by=['date_factor'],inplace=True)
    matches = matches.reset_index()

    winner_score = []

    for p in range(len(matches['winner_games'])):
        if((matches['winner_games'][p]-matches['loser_games'][p])>0):
            winner_score.append((matches['winner_games'][p]-matches['loser_games'][p])*matches['date_factor'][p])
        else:
            winner_score.append(0)

    matches['winner_score'] = winner_score

    wl = matches['winner'].tolist()
    ll = matches['loser'].tolist()
    all_players = set(wl + ll)
    all_players= sorted(all_players)

    matrix = pd.DataFrame(columns=all_players,index=all_players)

    for p1 in all_players:
        for p2 in all_players:
            matrix.at[p1,p2] = 0

    for i in range(len(matches)):
        matrix.at[matches['winner'][i],matches['loser'][i]] += matches['winner_score'][i]

    a = matrix
    b = np.matmul(a,a)
    c = a+b
    d = c.sum(axis=1)
    d = d.to_dict()

    ranking = pd.DataFrame()
    ranking_player = list(d.keys())
    ranking_power = list(d.values())
    ranking['Player'] = ranking_player
    ranking['Power'] = ranking_power

    ranking.sort_values("Power", ascending=False,inplace=True)
    ranking.Power = ranking.Power.round()
    ranking.reset_index(drop=True, inplace=True)
    ranking.drop(ranking[ranking['Power'] <= 0].index, inplace = True)

    player1 = ranking[ranking['Player'].str.contains(jugador1, case=False)]
    player2 = ranking[ranking['Player'].str.contains(jugador2, case=False)]

    result = {'Player 1': {'name':player1.Player.values[0],'win_percentage':round(player1.Power.values[0]/(player1.Power.values[0]+player2.Power.values[0]),2)},'Player 2': {'name':player2.Player.values[0],'win_percentage':round(player2.Power.values[0]/(player1.Power.values[0]+player2.Power.values[0]),2)}}

    return result