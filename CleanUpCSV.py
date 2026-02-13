import pandas as pd

position_cols = [
    "g_p","g_c","g_1b","g_2b","g_3b","g_ss",
    "g_lf","g_cf","g_rf","g_dh","g_ph","g_pr"
]

pos_map = {
    "g_p": "Pitcher", "g_c": "Catcher", "g_1b": "1st Base", "g_2b": "2nd Base",
    "g_3b": "3rd Base", "g_ss": "Short Stop", "g_lf": "Left Field",
    "g_cf": "Center Field", "g_rf": "Right Field", "g_dh": "Designated Hitter",
    "g_ph": "Pinch Hitter", "g_pr": "Pinch Runner"
}

team_dict = {
    "ARI": "Arizona Diamondbacks",#
    "ATL": "Atlanta Braves",#
    "BAL": "Baltimore Orioles",#
    "BOS": "Boston Red Sox",#
    "CHN": "Chicago Cubs",#
    "CHA": "Chicago White Sox",#
    "CIN": "Cincinnati Reds",#
    "CLE": "Cleveland Guardians",#
    "COL": "Colorado Rockies",#
    "DET": "Detroit Tigers",#
    "HOU": "Houston Astros",#
    "KCA": "Kansas City Royals",#
    "LAA": "Los Angeles Angels",
    "LAN": "Los Angeles Dodgers",#
    "MIA": "Miami Marlins",#
    "MIL": "Milwaukee Brewers",#
    "MIN": "Minnesota Twins",#
    "NYN": "New York Mets",#
    "NYA": "New York Yankees",#
    "ATH": "Oakland Athletics",#
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "SDN": "San Diego Padres",#
    "SFN": "San Francisco Giants",#
    "SEA": "Seattle Mariners",#
    "SLN": "St. Louis Cardinals",#
    "TBA": "Tampa Bay Rays",#
    "TEX": "Texas Rangers",#
    "TOR": "Toronto Blue Jays",#
    "WAS": "Washington Nationals",#
    #Old teams / negro league teams
    "BRG": "Brooklyn Royal Giants",
    "ACY": "Atlantic City Bacharach Giants",
    "BLS": "Baltimore Black Sox",
    "KCM": "Kansas City Monarchs",
    "WS1": "Washington Senators",
    "CAG": "Chicago American Giants"
    "MON": "Montreal Expos"
}

def extract_positions(row):
    return ",".join(
        pos_map[col] for col in position_cols if row[col] > 0
    )

def most_played_position(group):
    totals = group[position_cols].sum()
    best_col = totals.idxmax()
    return pos_map[best_col]

def cleanCSV():
    df = pd.read_csv("allplayers.csv")

    result = (
        df.groupby(["id", "last", "first"])
        .agg({
            "team": lambda x: ",".join(team_dict.get(t, t) for t in sorted(set(x))),
            "season": lambda x: ",".join(sorted(set(map(str, x)))),
            **{col: "sum" for col in position_cols}
        })
        .reset_index()
    )
    result["position"] = result.apply(
        lambda row: pos_map[row[position_cols].idxmax()],
        axis=1
    )
    result = result[["id", "last", "first", "team", "position", "season"]]

    result.to_csv("CleanedPlayers.csv", index=False)

def sortBySeason():
    df = pd.read_csv("CleanedPlayers.csv")
    df["first_season"] = df["season"].apply(
        lambda x: min(map(int, x.split(",")))
    )
    df = df.sort_values(by=["first_season", "last", "first"])
    df = df.drop(columns=["first_season"])
    df.to_csv("CleanedSorted.csv", index=False)


if __name__ == "__main__":
    while True:
        response = input("Press 1 if you want to clean up to CSV\nPress 2 if you want to sort the new CSV\nPress anything else to exit\n")
        if response == "1":
            print("Cleaning CSV...")
            cleanCSV()
            print("Complete")
        elif response == "2":
            print("Sorting CSV based on Season...")
            sortBySeason()
            print("Complete")
        else:
            print("Exiting...")
            break
