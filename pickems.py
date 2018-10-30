from nba_py import Scoreboard, constants
from nba_py.team import TeamSummary
from nba_py.game import BoxscoreSummary
import pandas as pd
import datetime
import requests

def find_team_name(id):
    teams = constants.TEAMS
    for team, stats in teams.items():
        for key, val in stats.items():
            if key == 'id' and val == str(id):
                return stats['name']

    return None

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(0, 7)]

games = pd.DataFrame(columns=Scoreboard().game_header().columns)
for date in date_list:
    print(date.day, date.month, date.year)
    games = games.append(Scoreboard(year=date.year, day=date.day,
                            month=date.month).game_header())

games['VISITOR_TEAM_STR'] = games['VISITOR_TEAM_ID'].apply(find_team_name)
games['HOME_TEAM_STR'] = games['HOME_TEAM_ID'].apply(find_team_name)
games['MARQUEE_STR'] = games['VISITOR_TEAM_STR'] + ' @ ' + games['HOME_TEAM_STR']

my_data={'home_teams': str(list(games['HOME_TEAM_STR'])).replace('\'','\"'),
                    'away_teams': str(list(games['VISITOR_TEAM_STR'])).replace('\'', '\"'),
                    'marquee_strs': str(list(games['MARQUEE_STR'])).replace('\'', '\"'),
                    'form_name': 'NBA Pickems - Week 3'}
print(my_data)

r = requests.post('https://script.google.com/macros/s/AKfycbwbvSTlii8PbnjiF7eEPxvvWw8dwMP4ZXJ9r7LgGxU_xn5EfBZV/exec',
              data=my_data)
print(r.text)
