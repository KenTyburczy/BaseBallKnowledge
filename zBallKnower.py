import csv
import random

with open("CleanedPlayers.csv", newline="") as f:
    reader = csv.DictReader(f)
    row = random.choice(list(reader))

player_id = row["id"]
last      = row["last"]
first     = row["first"]
team      = row["team"]
position  = row["position"]
season    = row["season"]

team_dict = {
    "Arizona Diamondbacks": "ARI",#
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC",
    "Chicago White Sox": "CHA",#
    "Cincinnati Reds": "CIN",#
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KCR",
    "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAN",
    "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Mets": "NYN",#
    "New York Yankees": "NYA",#
    "Oakland Athletics": "OAK",
    "Philadelphia Phillies": "PHI",#
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SDP",
    "San Francisco Giants": "SFG",
    "Seattle Mariners": "SEA",
    "St. Louis Cardinals": "SLN",#
    "Tampa Bay Rays": "TBR",
    "Texas Rangers": "TEX",#
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WSH"
}


positionDict

print(f"{first} {last} played for {team} as {position} in {season}")