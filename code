import random
import json
import os
import random

dateipfad = os.path.join(os.path.dirname(__file__), "teams.json")

teams = []  # speichert alle erstellten Teams

champions = [
    {"name": "Champion 1", "stärke": 90},
    {"name": "Champion 2", "stärke": 85},
    {"name": "Champion 3", "stärke": 80},
    {"name": "Champion 4", "stärke": 75},    
    {"name": "Champion 5", "stärke": 70},
    {"name": "Champion 6", "stärke": 65},
    {"name": "Champion 7", "stärke": 60},
    {"name": "Champion 8", "stärke": 55},
    {"name": "Champion 9", "stärke": 50},
    {"name": "Champion 10", "stärke": 45}
]

def spiel_berechnen(team_links, team_rechts, champs_links, champs_rechts):
    rollen = ["Top", "Jungle", "Mid", "Bot", "Support"]

    sw_links = {}
    sw_rechts = {}

    teamwert_links = 0
    teamwert_rechts = 0

    for rolle in rollen:
        # Werte holen
        p1 = team_links["spieler"][rolle]
        c1 = champs_links[rolle]

        p2 = team_rechts["spieler"][rolle]
        c2 = champs_rechts[rolle]

        # Formel
        sw1 = (c1["stärke"] * 0.5) + (p1["skill"] * 0.5) + random.randint(-10, 10)
        sw2 = (c2["stärke"] * 0.5) + (p2["skill"] * 0.5) + random.randint(-10, 10)

        # optional runden
        sw1 = round(sw1)
        sw2 = round(sw2)

        sw_links[rolle] = sw1
        sw_rechts[rolle] = sw2

        teamwert_links += sw1
        teamwert_rechts += sw2

    # Gewinner bestimmen
    if teamwert_links > teamwert_rechts:
        winner = "links"
    elif teamwert_rechts > teamwert_links:
        winner = "rechts"
    else:
        winner = random.choice(["links", "rechts"])

    return sw_links, sw_rechts, teamwert_links, teamwert_rechts, winner

def match_anzeige(team_links, team_rechts, champs_links=None, champs_rechts=None, sw_links=None, sw_rechts=None):
    rollen = ["Top", "Jungle", "Mid", "Bot", "Support"]

    # 🔹 Überschrift
    print(f"{team_links['name']} vs {team_rechts['name']}\n")

    # 🔹 Header (mit SW!)
    print(f"{'Rolle':<8} | {'Spieler':<18} | {'S':>3} | {'Champ':<12} | {'CS':>3} | {'SW':>4} || "
          f"{'Rolle':<8} | {'Spieler':<18} | {'S':>3} | {'Champ':<12} | {'CS':>3} | {'SW':>4} |")
    print("-" * 120)

    for rolle in rollen:
        p1 = team_links["spieler"][rolle]
        p2 = team_rechts["spieler"][rolle]

        # Champs
        champ1_name = champs_links[rolle]["name"] if champs_links else ""
        champ1_str = champs_links[rolle]["stärke"] if champs_links else ""

        champ2_name = champs_rechts[rolle]["name"] if champs_rechts else ""
        champ2_str = champs_rechts[rolle]["stärke"] if champs_rechts else ""

        # Spielerwerte
        sw1 = sw_links[rolle] if sw_links else ""
        sw2 = sw_rechts[rolle] if sw_rechts else ""

        print(f"{rolle:<8} | {team_links['tag']} {p1['name']:<14} | {p1['skill']:>3} | "
              f"{champ1_name:<12} | {champ1_str:>3} | {sw1:>4} || "
              f"{rolle:<8} | {team_rechts['tag']} {p2['name']:<14} | {p2['skill']:>3} | "
              f"{champ2_name:<12} | {champ2_str:>3} | {sw2:>4} |")

def team_ranked(eigenes_team):
    if len(teams) < 2:
        print("Nicht genug Teams vorhanden!")
        input("Enter drücken...")
        return

    gegner = random.choice([t for t in teams if t != eigenes_team])

    if random.choice([True, False]):
        team_links = eigenes_team
        team_rechts = gegner
    else:
        team_links = gegner
        team_rechts = eigenes_team

    # 🔹 SCHRITT 1
    print("\n=== MATCH GEFUNDEN ===\n")
    match_anzeige(team_links, team_rechts)

    input("\nEnter für Champion Auswahl...")

    # 🔹 SCHRITT 2 (HIER EINFÜGEN)
    champ_pool = sorted(champions, key=lambda c: c["stärke"], reverse=True)

    reihenfolge = [1,2,2,1,1,2,2,1,1,2]

    rollen = ["Top", "Jungle", "Mid", "Bot", "Support"]

    champs_links = {}
    champs_rechts = {}

    freie_rollen_links = rollen.copy()
    freie_rollen_rechts = rollen.copy()

    for i, pick in enumerate(reihenfolge):
        champ = champ_pool[i]

        if pick == 1:
            rolle = random.choice(freie_rollen_links)
            champs_links[rolle] = champ
            freie_rollen_links.remove(rolle)
        else:
            rolle = random.choice(freie_rollen_rechts)
            champs_rechts[rolle] = champ
            freie_rollen_rechts.remove(rolle)

    # 🔹 SCHRITT 2 ANZEIGE
    print("\n=== CHAMPIONS ZUGEWIESEN ===\n")
    match_anzeige(team_links, team_rechts, champs_links, champs_rechts)

    input("\nEnter für Spiel...")

    # 🔹 Spiel berechnen
    sw_links, sw_rechts, tw_links, tw_rechts, winner = spiel_berechnen(
    team_links, team_rechts, champs_links, champs_rechts
)

    # 🔹 Ergebnis-Header bauen
    if winner == "links":
        result_text = "GEWINNT"
    else:
        result_text = "VERLIERT"

    header = f"{team_links['name']} ({tw_links}) {result_text} gegen {team_rechts['name']} ({tw_rechts})"

    print(f"\n=== ERGEBNIS ===")
    print(header + "\n")

    # 🔹 Finale Anzeige mit SW
    match_anzeige(team_links, team_rechts, champs_links, champs_rechts, sw_links, sw_rechts)

    input("\nEnter zum Fortfahren...")

def champions_anzeigen(zurueck_funktion):
    while True:
        print("\n=== CHAMPION ÜBERSICHT ===\n")

        # alphabetisch sortieren
        sortiert = sorted(champions, key=lambda c: c["name"])

        # Header
        print(f"{'Name':<15} | {'Stärke':>7}")
        print("-" * 25)

        # Inhalte
        for champ in sortiert:
            print(f"{champ['name']:<15} | {champ['stärke']:>7}")

        print("\nx. Zurück")

        choice = input("Auswahl: ").strip().lower()

        if choice == "x":
            return

def teams_speichern():
    with open(dateipfad, "w") as f:
        json.dump(teams, f, indent=4)

def teams_laden():
    global teams
    try:
        with open(dateipfad, "r") as f:
            teams = json.load(f)
    except FileNotFoundError:
        teams = []


def team_waehlen():
    while True:
        print("\n=== TEAM WÄHLEN ===")

        # ❗ Keine Teams vorhanden
        if not teams:
            print("Keine Teams vorhanden!")
            input("Enter drücken...")
            return

        # 📋 Teams auflisten
        for i, team in enumerate(teams, start=1):
            print(f"{i}. {team['name']} ({team['tag']})")

        print("x. Zurück")

        choice = input("Auswahl: ").strip().lower()

        # 🔙 zurück ins Startmenü
        if choice == "x":
            return

        # 🔢 Auswahl prüfen
        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(teams):
                selected_team = teams[index]

                # 👉 Übersicht anzeigen
                team_anzeigen(selected_team)

                # 👉 ins Teammenü gehen
                team_menue(selected_team)
                return
            else:
                print("Ungültige Nummer!")
        else:
            print("Ungültige Eingabe!")

def team_menue(team):
    while True:
        print(f"\n=== TEAM MENÜ ({team['name']}) ===")
        print("1. Teamranked")
        print("2. Teamübersicht")
        print("3. Champions")
        print("x. Hauptmenü")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            team_ranked(team)

        elif choice == "2":
            team_anzeigen(team)

        elif choice == "3":
            champions_anzeigen(team_menue)

        elif choice == "x":
            return  # WICHTIG: kein break!

        else:
            print("Ungültige Eingabe!")

def team_anzeigen(team):
    print("\n=== TEAM ÜBERSICHT ===")
    print(f"Team: {team['name']}")
    print(f"Tag: {team['tag']}\n")

    # Header
    print(f"{'Rolle':<10} | {'Spieler':<20} | {'Stärke':>7}")
    print("-" * 45)

    # Inhalte
    for rolle, spieler in team["spieler"].items():
        name_mit_tag = f"{team['tag']} {spieler['name']}"
        print(f"{rolle:<10} | {name_mit_tag:<20} | {spieler['skill']:>7}")

    input("\nEnter drücken...")

def spielername_existiert(name):
    for team in teams:
        for spieler in team["spieler"].values():
            if spieler["name"].lower() == name.lower():
                return True
    return False

def team_erstellen():
    print("\n=== TEAM ERSTELLEN ===")

    # 🔤 Teamname
    while True:
        name = input("Teamname (1-30 Zeichen): ").strip()
        if 1 <= len(name) <= 30 and name not in [t["name"] for t in teams]:
            break
        print("Ungültiger oder bereits vergebener Name!")

    # 🔠 Abkürzung
    while True:
        tag = input("Team Abkürzung (1-3 Zeichen): ").strip().upper()
        if 1 <= len(tag) <= 3 and tag not in [t["tag"] for t in teams]:
            break
        print("Ungültige Abkürzung!")

    # 👥 Spieler erstellen
    rollen = ["Top", "Jungle", "Mid", "Bot", "Support"]
    spieler = {}

    for rolle in rollen:
        while True:
            name_spieler = input(f"{rolle} Spielername (1-30 Zeichen): ").strip()
            if (
                1 <= len(name_spieler) <= 30
                and not spielername_existiert(name_spieler)
                and name_spieler.lower() not in [p["name"].lower() for p in spieler.values()]
            ):
                spieler[rolle] = {
                    "name": name_spieler,
                    "skill": random.randint(1, 99)
                }
                break
            print("Ungültiger Name!")


    # Team als Objekt speichern
    team = {
        "name": name,
        "tag": tag,
        "spieler": spieler
    }

    teams.append(team)

    # 👉 Team Speichern
    teams_speichern()

    # 👉 einmalige Anzeige direkt nach der Erstellung
    team_anzeigen(team)

    # 👉 direkt ins Teammenü springen
    team_menue(team)

def start_menu():
    while True:
        print("\n=== STARTMENÜ ===")
        print("1. Team wählen")
        print("2. Team erstellen")
        print("3. Champions")
        print("x. Beenden")

        choice = input("Auswahl: ").strip().lower()

        if choice == "1":
            team_waehlen()
        
        elif choice == "2":
            team_erstellen()

        elif choice == "3":
            champions_anzeigen(start_menu)
        
        elif choice == "x":
            print("Spiel wird beendet...")
            break
        
        else:
            print("Ungültige Eingabe!")
            input("Weiter mit Enter...")


# Startpunkt des Programms
if __name__ == "__main__":
    teams_laden()
    start_menu()
