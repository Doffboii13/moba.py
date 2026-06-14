import random
import json
import os
import random

# ANSI Farbcodes
ROT = "\033[91m"
GELB = "\033[93m"
GRÜN = "\033[92m"
RESET = "\033[0m"

dateipfad = os.path.join(os.path.dirname(__file__), "teams.json")
matches_dateipfad = os.path.join(os.path.dirname(__file__), "matches.json")

teams = []  # speichert alle erstellten Teams
matches = []  # speichert alle Spiele

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
    """Berechnet die Spielwerte pro Rolle und bestimmt den Gewinner"""
    rollen = ["Top", "Jungle", "Mid", "Bot", "Support"]

    sw_links = {}
    sw_rechts = {}
    
    luck_links = {}
    luck_rechts = {}

    teamwert_links = 0
    teamwert_rechts = 0

    for rolle in rollen:
        # Werte der Spieler und Champions holen
        p1 = team_links["spieler"][rolle]
        c1 = champs_links[rolle]

        p2 = team_rechts["spieler"][rolle]
        c2 = champs_rechts[rolle]

        # Zufallsglück für beide Teams
        luck1 = random.randint(-10, 10)
        luck2 = random.randint(-10, 10)

        # Formel: Champion-Stärke (50%) + Spieler-Skill (50%) + Glück
        sw1 = (c1["stärke"] * 0.5) + (p1["skill"] * 0.5) + luck1
        sw2 = (c2["stärke"] * 0.5) + (p2["skill"] * 0.5) + luck2

        # Werte runden
        sw1 = round(sw1)
        sw2 = round(sw2)

        sw_links[rolle] = sw1
        sw_rechts[rolle] = sw2
        
        luck_links[rolle] = luck1
        luck_rechts[rolle] = luck2

        teamwert_links += sw1
        teamwert_rechts += sw2

    # Gewinner bestimmen (höherer Teamwert gewinnt)
    if teamwert_links > teamwert_rechts:
        winner = "links"
    elif teamwert_rechts > teamwert_links:
        winner = "rechts"
    else:
        winner = random.choice(["links", "rechts"])

    return sw_links, sw_rechts, luck_links, luck_rechts, teamwert_links, teamwert_rechts, winner

def get_farbe_für_sw(rolle, luck_wert, luck_links, luck_rechts, winner):
    """Bestimmt die Farbe für einen SW-Wert basierend auf Glück und Gewinner"""
    
    # Höchstes Glück im Siegerteam finden
    if winner == "links":
        max_luck = max(luck_links.values())
        ist_max_luck = luck_links[rolle] == max_luck
    else:
        max_luck = max(luck_rechts.values())
        ist_max_luck = luck_rechts[rolle] == max_luck
    
    # Farblogik: Gelb (Höchstes Glück) > Grün (Positiv) > Rot (Negativ)
    if ist_max_luck:
        return GELB
    elif luck_wert > 0:
        return GRÜN
    elif luck_wert < 0:
        return ROT
    else:
        return RESET  # 0 = keine Farbe

def match_anzeige(team_links, team_rechts, champs_links=None, champs_rechts=None, sw_links=None, sw_rechts=None, luck_links=None, luck_rechts=None, winner=None):
    """Zeigt beide Teams mit Spielern, Champions und Spielwerten side-by-side an"""
    rollen = ["Top", "Jungle", "Mid", "Bot", "Support"]

    # Überschrift mit Team-Namen
    print(f"{team_links['name']} vs {team_rechts['name']}\n")

    # Tabellen-Header
    print(f"{'Rolle':<8} | {'Spieler':<18} | {'S':>3} | {'Champ':<12} | {'CS':>3} | {'SW':>4} || "
          f"{'Rolle':<8} | {'Spieler':<18} | {'S':>3} | {'Champ':<12} | {'CS':>3} | {'SW':>4} |")
    print("-" * 120)

    for rolle in rollen:
        p1 = team_links["spieler"][rolle]
        p2 = team_rechts["spieler"][rolle]

        # Champion-Daten abrufen
        champ1_name = champs_links[rolle]["name"] if champs_links else ""
        champ1_str = champs_links[rolle]["stärke"] if champs_links else ""

        champ2_name = champs_rechts[rolle]["name"] if champs_rechts else ""
        champ2_str = champs_rechts[rolle]["stärke"] if champs_rechts else ""

        # Spielwert-Daten abrufen
        sw1 = sw_links[rolle] if sw_links else ""
        sw2 = sw_rechts[rolle] if sw_rechts else ""

        # SW-Werte mit Farben formatieren (nur wenn alle Daten vorhanden)
        if luck_links and winner:
            farbe1 = get_farbe_für_sw(rolle, luck_links[rolle], luck_links, luck_rechts, winner)
            farbe2 = get_farbe_für_sw(rolle, luck_rechts[rolle], luck_links, luck_rechts, winner)
            
            sw1_farbig = f"{farbe1}{sw1}{RESET}"
            sw2_farbig = f"{farbe2}{sw2}{RESET}"
        else:
            sw1_farbig = sw1
            sw2_farbig = sw2

        print(f"{rolle:<8} | {team_links['tag']} {p1['name']:<14} | {p1['skill']:>3} | "
              f"{champ1_name:<12} | {champ1_str:>3} | {sw1_farbig:>4} || "
              f"{rolle:<8} | {team_rechts['tag']} {p2['name']:<14} | {p2['skill']:>3} | "
              f"{champ2_name:<12} | {champ2_str:>3} | {sw2_farbig:>4} |")

def teams_speichern():
    """Speichert alle Teams in die JSON-Datei"""
    with open(dateipfad, "w") as f:
        json.dump(teams, f, indent=4)

def teams_laden():
    """Lädt alle Teams aus der JSON-Datei oder initialisiert leere Liste"""
    global teams
    try:
        with open(dateipfad, "r") as f:
            teams = json.load(f)
    except FileNotFoundError:
        teams = []

def matches_speichern():
    """Speichert alle Matches in die JSON-Datei"""
    with open(matches_dateipfad, "w") as f:
        json.dump(matches, f, indent=4)

def matches_laden():
    """Lädt alle Matches aus der JSON-Datei oder initialisiert leere Liste"""
    global matches
    try:
        with open(matches_dateipfad, "r") as f:
            matches = json.load(f)
    except FileNotFoundError:
        matches = []

def match_speichern(match_data):
    """Speichert ein einzelnes Match und aktualisiert die Datei"""
    matches.append(match_data)
    matches_speichern()

def champions_anzeigen(zurueck_funktion):
    """Zeigt alle Champions sortiert nach Name mit ihren Stärkewerten an"""
    while True:
        print("\n=== CHAMPION ÜBERSICHT ===\n")

        # Alphabetisch sortieren
        sortiert = sorted(champions, key=lambda c: c["name"])

        # Tabellen-Header
        print(f"{'Name':<15} | {'Stärke':>7}")
        print("-" * 25)

        # Alle Champions auflisten
        for champ in sortiert:
            print(f"{champ['name']:<15} | {champ['stärke']:>7}")

        print("\nx. Zurück")

        choice = input("Auswahl: ").strip().lower()

        if choice == "x":
            return

def team_ranked(eigenes_team):
    """Simuliert ein Ranked-Match: Gegner wählen, Champions picken, Ergebnis berechnen"""
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

    # Match-Übersicht anzeigen (ohne Champions und Spielwerte)
    print("\n=== MATCH GEFUNDEN ===\n")
    match_anzeige(team_links, team_rechts)

    input("\nEnter für Champion Auswahl...")

    # Champion-Picking: Wechselweise Champions aus dem Pool auswählen
    champ_pool = sorted(champions, key=lambda c: c["stärke"], reverse=True)

    reihenfolge = [1,2,2,1,1,2,2,1,1,2]  # Pick-Reihenfolge (1=Team links, 2=Team rechts)

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

    # Champions mit Rollen-Zuordnung anzeigen
    print("\n=== CHAMPIONS ZUGEWIESEN ===\n")
    match_anzeige(team_links, team_rechts, champs_links, champs_rechts)

    input("\nEnter für Spiel...")

    # Spielwerte berechnen und Gewinner bestimmen
    sw_links, sw_rechts, luck_links, luck_rechts, tw_links, tw_rechts, winner = spiel_berechnen(
        team_links, team_rechts, champs_links, champs_rechts
    )

    # Ergebnis-Text basierend auf Gewinner
    if winner == "links":
        result_text = "GEWINNT"
    else:
        result_text = "VERLIERT"

    header = f"{team_links['name']} ({tw_links}) {result_text} gegen {team_rechts['name']} ({tw_rechts})"

    print(f"\n=== ERGEBNIS ===")
    print(header + "\n")

    # Finale Anzeige mit Spielwerten und Farbcodierung
    match_anzeige(team_links, team_rechts, champs_links, champs_rechts, sw_links, sw_rechts, luck_links, luck_rechts, winner)

    input("\nEnter zum Fortfahren...")

    # Match speichern
    match_data = {
        "match_id": len(matches) + 1,
        "team_links": {"name": team_links["name"], "tag": team_links["tag"]},
        "team_rechts": {"name": team_rechts["name"], "tag": team_rechts["tag"]},
        "champs_links": champs_links,
        "champs_rechts": champs_rechts,
        "sw_links": sw_links,
        "sw_rechts": sw_rechts,
        "luck_links": luck_links,
        "luck_rechts": luck_rechts,
        "tw_links": tw_links,
        "tw_rechts": tw_rechts,
        "winner": winner
    }
    match_speichern(match_data)

def team_waehlen():
    """Zeigt alle Teams an und lässt den Spieler eines wählen"""
    while True:
        print("\n=== TEAM WÄHLEN ===")

        # Prüfung: Keine Teams vorhanden
        if not teams:
            print("Keine Teams vorhanden!")
            input("Enter drücken...")
            return

        # Alle Teams auflisten
        for i, team in enumerate(teams, start=1):
            print(f"{i}. {team['name']} ({team['tag']})")

        print("x. Zurück")

        choice = input("Auswahl: ").strip().lower()

        # Zurück zum Startmenü
        if choice == "x":
            return

        # Auswahl validieren
        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(teams):
                selected_team = teams[index]

                # Team-Übersicht anzeigen
                team_anzeigen(selected_team)

                # Ins Team-Menü wechseln
                team_menue(selected_team)
                return
            else:
                print("Ungültige Nummer!")
        else:
            print("Ungültige Eingabe!")

def team_menue(team):
    """Menü für Team-Aktionen: Ranked spielen, Team ansehen oder Champions"""
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
            return

        else:
            print("Ungültige Eingabe!")

def team_anzeigen(team):
    """Zeigt Teamübersicht mit allen Spielern, deren Rollen und Skills"""
    print("\n=== TEAM ÜBERSICHT ===")
    print(f"Team: {team['name']}")
    print(f"Tag: {team['tag']}\n")

    # Tabellen-Header
    print(f"{'Rolle':<10} | {'Spieler':<20} | {'Stärke':>7}")
    print("-" * 45)

    # Alle Spieler mit ihren Daten auflisten
    for rolle, spieler in team["spieler"].items():
        name_mit_tag = f"{team['tag']} {spieler['name']}"
        print(f"{rolle:<10} | {name_mit_tag:<20} | {spieler['skill']:>7}")

    input("\nEnter drücken...")

def spielername_existiert(name):
    """Prüft, ob ein Spieler-Name bereits in einem anderen Team existiert"""
    for team in teams:
        for spieler in team["spieler"].values():
            if spieler["name"].lower() == name.lower():
                return True
    return False

def team_erstellen():
    """Erstellt ein neues Team mit Namen, Tag und 5 Spielern für alle Rollen"""
    print("\n=== TEAM ERSTELLEN ===")

    # Teamname eingeben
    while True:
        name = input("Teamname (1-30 Zeichen): ").strip()
        if 1 <= len(name) <= 30 and name not in [t["name"] for t in teams]:
            break
        print("Ungültiger oder bereits vergebener Name!")

    # Team-Abkürzung eingeben
    while True:
        tag = input("Team Abkürzung (1-3 Zeichen): ").strip().upper()
        if 1 <= len(tag) <= 3 and tag not in [t["tag"] for t in teams]:
            break
        print("Ungültige Abkürzung!")

    # Spieler für alle 5 Rollen erstellen
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

    # Team-Daten speichern
    team = {
        "name": name,
        "tag": tag,
        "spieler": spieler
    }

    teams.append(team)

    # Team in JSON-Datei speichern
    teams_speichern()

    # Neu erstelltes Team anzeigen
    team_anzeigen(team)

    # Direkt ins Team-Menü wechseln
    team_menue(team)

def start_menu():
    """Hauptmenü: Team wählen/erstellen, Champions anschauen oder Spiel beenden"""
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
    matches_laden()
    start_menu()
