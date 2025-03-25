import requests, json
from datetime import datetime

def match_time(datetime_str):
    datetime_obj = datetime.fromisoformat(datetime_str)
    yearpart = datetime_obj.date().isoformat()  # تحويل التاريخ إلى سلسلة نصية
    timepart = datetime_obj.time().strftime('%H:%M')  # تحويل الوقت إلى سلسلة نصية بالتنسيق المطلوب
    return yearpart, timepart


def logo_maker(id):
    link = f'https://imagecache.365scores.com/image/upload/f_png,w_30,h_30,c_limit,q_auto:eco,dpr_3,d_Competitors:default1.png/v6/Competitors/{id}'
    return link


gameId = 4299793
gameinfo = (
    'https://webws.365scores.com/web/game/?'
    'appTypeId=5&'
    'langId=27&'
    'timezoneName=Asia/Riyadh&'
    'userCountryId=122&'
    f'gameId={gameId}&'
)
headers = {
        'dnt': '1',
        'origin': 'https://www.365scores.com',
        'referer': 'https://www.365scores.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }
# https://football-api.alameedtv.workers.dev/v1/json_format/gameinfo?gameid=4390966
r = requests.get(gameinfo, headers=headers)
r = r.json()
eventsList = []

members = r['game']['members']
events = r['game']['events']
eventsList = []
for event in events:
    gameTime = event['gameTime']
    extratime = event['addedTime']
    eventTime = gameTime + extratime
    playerID = event['playerId']
    TEAMid = event['competitorId']
    eventName = event['eventType']['name']
    if eventName == 'Woodwork':
        eventName = 'تسديدة في العارضة'
    if eventName == 'Substitution':
        playerID2 = event['extraPlayers'][0]
        for member in members:
            check_id = member.get('id', None)
            if check_id is None:
                continue
            if member['id'] == playerID:
                playerIN = member['name']
            if member['id'] == playerID2:
                playerOUT = member['name']
        eventsList.append({'eventTime':eventTime, 'teamID':TEAMid, 'event': 'تبديل', 'playerIN': playerIN, 'playerOUT': playerOUT})

    elif eventName == 'هدف':
        subTypeName = event['eventType']['subTypeName']
        for member in members:
            check_id = member.get('id', None)
            if check_id is None:
                continue
            elif member['id'] == playerID:
                player = member['name']
        if subTypeName == 'ركلة جزاء':
            eventsList.append({'eventTime':eventTime, 'teamID':TEAMid, 'event': f'هدف {subTypeName}', 'player': player})
        elif subTypeName == 'هدف ذاتي':
            eventsList.append({'eventTime':eventTime, 'teamID':TEAMid, 'event': 'هدف عكسي', 'player': player})
        else:
            eventsList.append({'eventTime':eventTime, 'teamID':TEAMid, 'event': 'هدف', 'player': player})
    else:
        for member in members:
            check_id = member.get('id', None)
            if check_id is None:
                continue
            if member['id'] == playerID:
                player = member['name']
        #print(f'{eventTime} {player} {eventName}')
        eventsList.append({'eventTime':eventTime, 'teamID':TEAMid, 'event': eventName, 'player': player})

gamelist = []

game = r['game']
competitionId = game['competitionId']
aggregateText = game.get('aggregateText', None)
winDescription = game.get('winDescription', None)
competitionDisplayName = game['competitionDisplayName']
statusText = game['statusText']
startyear, startTime = match_time(game['startTime'])
gameTime = game['gameTime']
UniqueID = game['id']
if gameTime == -1:
    gameTime = ""
first_team = game['homeCompetitor']['name']
first_team_id = game['homeCompetitor']['id']
first_team_logo = logo_maker(game['homeCompetitor']['id'])
second_team = game['awayCompetitor']['name']
second_team_id = game['awayCompetitor']['id']
second_team_logo = logo_maker(game['awayCompetitor']['id'])
first_team_score = game['homeCompetitor']['score']
if first_team_score == -1:
    first_team_score = 0
second_team_score = game['awayCompetitor']['score']
if second_team_score == -1:
    second_team_score = 0

game_data = {
    'id': UniqueID,
    'competitionId': competitionId,
    'competitionDisplayName': competitionDisplayName,
    'statusText': statusText,
    'startTime': startTime,
    'startyear': startyear,
    'gameTime': gameTime,
    'first_team': first_team,
    'first_team_id': first_team_id,
    'first_team_logo': first_team_logo,
    'second_team': second_team,
    'second_team_id': second_team_id,
    'second_team_logo': second_team_logo,
    'first_team_score': first_team_score,
    'second_team_score': second_team_score,
    'aggregateText': aggregateText,
    'winDescription': winDescription
}
gamelist.append(game_data)

respons_data = {
    'events': eventsList,
    'games': gamelist
}

print(respons_data['events'])