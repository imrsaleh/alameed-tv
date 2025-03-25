from js import Response, Headers
from pyodide.http import pyfetch
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs


def match_time(datetime_str):
    datetime_obj = datetime.fromisoformat(datetime_str)
    yearpart = datetime_obj.date().isoformat()  # تحويل التاريخ إلى سلسلة نصية
    timepart = datetime_obj.time().strftime('%H:%M')  # تحويل الوقت إلى سلسلة نصية بالتنسيق المطلوب
    return yearpart, timepart


def logo_maker(id):
    link = f'https://imagecache.365scores.com/image/upload/f_png,w_30,h_30,c_limit,q_auto:eco,dpr_3,d_Competitors:default1.png/v6/Competitors/{id}'
    return link


def create_event_data(eventTime, TEAMid, eventName, player=None, playerIN=None, playerOUT=None):
    """
    إنشاء بيانات الحدث بناءً على المدخلات.
    """
    event_data = {'eventTime': eventTime, 'teamID': TEAMid, 'event': eventName}
    if player:
        event_data['player'] = player
    if playerIN and playerOUT:
        event_data['playerIN'] = playerIN
        event_data['playerOUT'] = playerOUT
    return event_data


# https://football-api.alameedtv.workers.dev/v1/json_format
async def on_fetch(request):
    reqURL = request.url
    if not reqURL.startswith('https://football-api.alameedtv.workers.dev/v1/'):
        return Response.new('Not Found', status=404)
    
    parseurl = urlparse(reqURL)
    query_params = parse_qs(parseurl.query)
    teamid = query_params.get("teamid", [None])[0]
    league = query_params.get("league", [None])[0]
    gameId = query_params.get("gameid", [None])[0]
    headers = {
        'dnt': '1',
        'origin': 'https://www.365scores.com',
        'referer': 'https://www.365scores.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }
    if teamid != None:
        current = ('https://webws.365scores.com/web/games/current/?'
                'appTypeId=5&'
                'langId=27&'
                'timezoneName=Asia/Riyadh&'
                'userCountryId=122&'
                f'competitors={teamid}&'
                'showOdds=true')
        r = await pyfetch(current, headers=headers)
    elif league != None: 
        fixtures = ('https://webws.365scores.com/web/games/fixtures/?'
            'appTypeId=5&'
            'langId=27&'
            'timezoneName=Asia/Riyadh&'
            'userCountryId=122&'
            f'competitions={league}&'
            'showOdds=true&'
            'includeTopBettingOpportunity=1')
        r = await pyfetch(fixtures, headers=headers)
    elif gameId != None:
        gameinfo = (
            'https://webws.365scores.com/web/game/?'
            'appTypeId=5&'
            'langId=27&'
            'timezoneName=Asia/Riyadh&'
            'userCountryId=122&'
            f'gameId={gameId}&'
        )
        # https://football-api.alameedtv.workers.dev/v1/json_format/gameinfo?gameid=4390966
        r = await pyfetch(gameinfo, headers=headers)
        r = await r.json()
        eventsList = []
        try:
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
                    playerIN, playerOUT = None, None
                    for member in members:
                        check_id = member.get('id', None)
                        if check_id is None:
                            continue
                        if member['id'] == playerID:
                            playerIN = member['name']
                        if member['id'] == playerID2:
                            playerOUT = member['name']
                    eventsList.append(create_event_data(eventTime, TEAMid, 'تبديل', playerIN=playerIN, playerOUT=playerOUT))

                elif eventName == 'هدف':
                    subTypeName = event['eventType']['subTypeName']
                    player = None
                    for member in members:
                        check_id = member.get('id', None)
                        if check_id is None:
                            continue
                        elif member['id'] == playerID:
                            player = member['name']
                    if subTypeName == 'ركلة جزاء':
                        eventsList.append(create_event_data(eventTime, TEAMid, f'هدف {subTypeName}', player=player))
                    elif subTypeName == 'هدف ذاتي':
                        eventsList.append(create_event_data(eventTime, TEAMid, 'هدف عكسي', player=player))
                    else:
                        eventsList.append(create_event_data(eventTime, TEAMid, 'هدف', player=player))

                else:
                    player = None
                    for member in members:
                        check_id = member.get('id', None)
                        if check_id is None:
                            continue
                        if member['id'] == playerID:
                            player = member['name']
                    eventsList.append(create_event_data(eventTime, TEAMid, eventName, player=player))

        except KeyError as e:
            print(f"Missing key: {e}")
            eventsList.append({'eventTime': None, 'teamID': None, 'event': None, 'player': None})
        except Exception as e:
            print(f"An error occurred: {e}")
            eventsList.append({'eventTime': None, 'teamID': None, 'event': None, 'player': None})

        gamelist = []
        try:
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
        except:
            game_data = {
                'id': None,
                'competitionId': None,
                'competitionDisplayName': None,
                'statusText': None,
                'startTime': None,
                'startyear': None,
                'gameTime': None,
                'first_team': None,
                'first_team_id': None,
                'first_team_logo': None,
                'second_team': None,
                'second_team_id': None,
                'second_team_logo': None,
                'first_team_score': None,
                'second_team_score': None,
                'aggregateText': None,
                'winDescription': None
            }
            gamelist.append(game_data)

        respons_data = {
            'events': eventsList,
            'games': gamelist
        }

        data = json.dumps(respons_data)
        headers = Headers.new({
            "content-type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
            }.items())
        return Response.new(data, headers=headers)

    else:  # مباريات اليوم
        today = datetime.now()
        startDate = today.strftime("%d/%m/%Y")
        day_after_tomorrow = today + timedelta(days=10)
        yeasterday_format = today + timedelta(days=-4)
        yeasterday = yeasterday_format.strftime("%d/%m/%Y")
        endDate = day_after_tomorrow.strftime("%d/%m/%Y")
                                                                                                                                                
        competitions = '572,573,568,649,7,11,5501,623,17,13,37,5930,6196,605,6316,9,613,645,5421,5096,7016'
        competitors = '54729,22288,480,469,465,331,333,341'

        the_api = ('https://webws.365scores.com/web/games/myscores/?'
                'appTypeId=5&'
                'langId=27&'
                'timezoneName=Asia/Riyadh&'
                'userCountryId=122&'
                f'competitions={competitions}&'
                f'competitors={competitors}&'
                f'startDate={yeasterday}&'
                f'endDate={endDate}&'
                'showOdds=true&'
                'withSuggested=true')
        #print(the_api)
        r = await pyfetch(the_api, headers=headers)

    games = await r.json()
    list_data = []
    for game in games['games']:
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
        list_data.append(game_data)

    respons_data = {'games': list_data}

    

    data = json.dumps(respons_data)
    headers = Headers.new({
            "content-type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
            }.items())
    return Response.new(data, headers=headers)
