import csv
import random

def randomPlayer():
    with open("Data/CleanedPlayers.csv", newline="") as f:
        reader = csv.DictReader(f)
        row = random.choice(list(reader))

    player_id = row["id"]
    last      = row["last"]
    first     = row["first"]
    team      = row["team"]
    position  = row["position"]
    season    = row["season"]

    
    print(f" This player played for {team} as {position} in {season}")
    answer = input('Input your guess: ')
    if answer == last + ' ' + first:
        print('Congrats! You got it right!')
    else:
        print('Sorry thats not correct. The correct answer is ' + first + ' ' + last)

def chooseEra():
    print('era')

def chooseTeam():
    print('team')

if __name__ == "__main__":

    print('1. Guess the Player\n2. Chose an Era\n3. Chose a Team\n4. Exit')
    frontpageOptions = input('Select option: ')
    if frontpageOptions == '1':
        randomPlayer()
    elif frontpageOptions == '2':
        chooseEra()
    elif frontpageOptions == '3':
        chooseTeam()
    else:
        exit