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

print(f"{first} {last} played for {team} as {position} in {season}")