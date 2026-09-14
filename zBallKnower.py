import random
import pyodbc

DB_PATH = r"C:\Users\kenty\Downloads\lahman_1871-2025.mdb"


def get_connection():
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={DB_PATH};"
    )
    return pyodbc.connect(conn_str)


def fetch_clue_pool(conn):
    """
    One row per player/season/team/position, used to generate the guessing clue.
    Pulled from Fielding since it has position + team + year together.
    Joined to Teams (on teamID + yearID) to get the full franchise name for that season.
    """
    query = """
        SELECT p.playerID, p.nameFirst, p.nameLast, t.name, f.POS, f.yearID
        FROM (Fielding AS f
        INNER JOIN People AS p ON f.playerID = p.playerID)
        INNER JOIN Teams AS t ON f.teamID = t.teamID AND f.yearID = t.yearID
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def is_pitcher(conn, player_id):
    query = "SELECT COUNT(*) FROM Pitching WHERE playerID = ?"
    cursor = conn.cursor()
    cursor.execute(query, player_id)
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0


def get_pitching_career(conn, player_id):
    query = """
        SELECT p.yearID, t.name, p.stint, p.W, p.L, p.G, p.GS, p.CG, p.SHO, p.SV,
               p.IPOuts, p.H, p.ER, p.HR, p.BB, p.SO, p.ERA
        FROM Pitching AS p
        INNER JOIN Teams AS t ON p.teamID = t.teamID AND p.yearID = t.yearID
        WHERE p.playerID = ?
        ORDER BY p.yearID, p.stint
    """
    cursor = conn.cursor()
    cursor.execute(query, player_id)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_batting_career(conn, player_id):
    # Note: Access needs [2B]/[3B] in brackets, not quotes, since they start with a digit
    query = """
        SELECT b.yearID, t.name, b.stint, b.G, b.AB, b.R, b.H, b.[2B], b.[3B], b.HR, b.RBI,
               b.SB, b.CS, b.BB, b.SO
        FROM Batting AS b
        INNER JOIN Teams AS t ON b.teamID = t.teamID AND b.yearID = t.yearID
        WHERE b.playerID = ?
        ORDER BY b.yearID, b.stint
    """
    cursor = conn.cursor()
    cursor.execute(query, player_id)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def print_pitching_career(rows):
    print("\nCareer Pitching Stats:")
    print(f"{'YEAR':<6}{'TEAM':<25}{'W':<4}{'L':<4}{'G':<4}{'GS':<4}{'CG':<4}"
          f"{'SHO':<5}{'SV':<4}{'IP':<7}{'H':<5}{'ER':<5}{'HR':<4}{'BB':<5}{'SO':<5}{'ERA':<6}")
    for yearID, teamName, stint, W, L, G, GS, CG, SHO, SV, IPOuts, H, ER, HR, BB, SO, ERA in rows:
        ip = (IPOuts or 0) / 3
        era = ERA if ERA is not None else 0
        print(f"{yearID:<6}{teamName:<25}{W or 0:<4}{L or 0:<4}{G or 0:<4}{GS or 0:<4}"
              f"{CG or 0:<4}{SHO or 0:<5}{SV or 0:<4}{ip:<7.1f}{H or 0:<5}{ER or 0:<5}"
              f"{HR or 0:<4}{BB or 0:<5}{SO or 0:<5}{era:<6.2f}")


def print_batting_career(rows):
    print("\nCareer Batting / Baserunning Stats:")
    print(f"{'YEAR':<6}{'TEAM':<25}{'G':<4}{'AB':<5}{'R':<4}{'H':<4}{'2B':<4}"
          f"{'3B':<4}{'HR':<4}{'RBI':<5}{'SB':<4}{'CS':<4}{'BB':<4}{'SO':<4}")
    for yearID, teamName, stint, G, AB, R, H, doubles, triples, HR, RBI, SB, CS, BB, SO in rows:
        print(f"{yearID:<6}{teamName:<25}{G or 0:<4}{AB or 0:<5}{R or 0:<4}{H or 0:<4}"
              f"{doubles or 0:<4}{triples or 0:<4}{HR or 0:<4}{RBI or 0:<5}"
              f"{SB or 0:<4}{CS or 0:<4}{BB or 0:<4}{SO or 0:<4}")


def randomPlayer(conn, clue_pool):
    player_id, first, last, team, position, season = random.choice(clue_pool)

    print(f"\nThis player was a {position}")

    if is_pitcher(conn, player_id):
        rows = get_pitching_career(conn, player_id)
        print_pitching_career(rows)
    else:
        rows = get_batting_career(conn, player_id)
        print_batting_career(rows)

    answer = input('\nInput your guess: ').strip().lower()
    correct = f"{last} {first}".strip().lower()

    if answer == correct:
        print('Congrats! You got it right!')
    else:
        print(f'Sorry thats not correct. The correct answer is {first} {last}')


def chooseEra():
    print('era')


def chooseTeam():
    print('team')


if __name__ == "__main__":
    conn = get_connection()
    clue_pool = fetch_clue_pool(conn)

    while True:
        print('1. Guess the Player\n2. Chose an Era\n3. Chose a Team\n4. Exit')
        frontpageOptions = input('Select option: ')
        if frontpageOptions == '1':
            randomPlayer(conn, clue_pool)
        elif frontpageOptions == '2':
            chooseEra()
        elif frontpageOptions == '3':
            chooseTeam()
        else:
            break

        playAgain = input('Want to try again?(Y/N) ')
        if playAgain.strip().upper() != 'Y':
            break

    conn.close()