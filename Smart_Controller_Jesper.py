def aantal_dagen(inputbestand):
    """Laat zien hoeveel dagen er in het invoerbestand staan en toon alleen de data (zonder header)."""

    try:
        with open(inputbestand, "r") as f:
            regels = [r.strip() for r in f if r.strip()]
    except FileNotFoundError:
        print(f"  Bestand '{inputbestand}' is niet gevonden.")
        print("Controleer of het bestand in dezelfde map staat als dit programma.")
        return

    if len(regels) <= 1:
        print("  Het invoerbestand is leeg of bevat geen data.")
        return

    # Eerste regel is de header, die slaan we over
    data = regels[1:]

    # Aantal dagen tonen
    print(f"\nAantal dagen gevonden: {len(data)}\n")

    # Elke regel netjes tonen
    for regel in data:
        print(regel)


    return len(data)

import os

def auto_bereken(inputbestand, outputbestand):
    """Leest het invoerbestand, berekent automatisch de waardes en slaat ze op in output.txt."""
    print("\n--- OPTIE 2: AUTOMATISCH BEREKENEN ---")
    print("Let op:")
    print("Deze optie berekent alles opnieuw op basis van het invoerbestand (input.txt).")
    print("Alle eerder handmatig aangepaste waarden in output.txt worden overschreven.\n")

    print("--- AUTOMATISCHE BEREKENING START ---")
    print("Het programma gaat nu op basis van de invoerdata bepalen:")
    print("  - Hoe hard de CV moet werken")
    print("  - Hoe hoog de ventilatie moet staan")
    print("  - Of de bewatering aan of uit moet\n")

    # Controleer of het invoerbestand bestaat
    if not os.path.exists(inputbestand):
        print(f"  Bestand '{inputbestand}' is niet gevonden. Zorg dat het in dezelfde map staat als dit programma.")
        return

    # Vraag eerst of we het bestaande outputbestand willen overschrijven
    if os.path.exists(outputbestand):
        antwoord = input(f"Er bestaat al een bestand '{outputbestand}'. Wil je dit overschrijven? (j/n): ").strip().lower()
        if antwoord != "j":
            print("Opslaan geannuleerd. De bestaande handmatige instellingen blijven behouden.\n")
            return

    # Lees de invoerregels
    with open(inputbestand, "r") as invoer:
        regels = [r.strip() for r in invoer if r.strip()]

    # Verwijder de header (eerste regel)
    regels = regels[1:]
    if not regels:
        print("  Geen gegevens gevonden in het invoerbestand.")
        return

    print("Berekenen van instellingen per dag...\n")
    uit = []

    for regel in regels:
        try:
            datum, personen, setpoint, buiten, neerslag = regel.split()
            personen = int(personen)
            setpoint = float(setpoint)
            buiten = float(buiten)
            neerslag = float(neerslag)
        except ValueError:
            print(f"  Ongeldige regel gevonden: '{regel}'. Wordt overgeslagen.")
            continue

        # CV-ketel berekening
        verschil = setpoint - buiten
        if verschil >= 20:
            cv = 100
        elif verschil >= 10:
            cv = 50
        else:
            cv = 0

        # Ventilatie berekening
        ventilatie = personen + 1
        if ventilatie > 4:
            ventilatie = 4

        # Bewatering berekening
        bewatering = neerslag < 3

        # Print per dag wat het programma berekent
        print(f"{datum}: CV={cv}%, Ventilatie={ventilatie}, Bewatering={bewatering}")

        # Voeg de resultaten toe aan de outputlijst
        uit.append(f"{datum};{cv};{ventilatie};{bewatering}")

    # Sla de resultaten op in het outputbestand
    print("\nDe berekende resultaten worden nu opgeslagen in het bestand 'output.txt'...")
    with open(outputbestand, "w") as out:
        for regel in uit:
            out.write(regel + "\n")

    print(f"\n De berekening is voltooid en opgeslagen in '{outputbestand}'.")
    print(f"Aantal verwerkte dagen: {len(uit)}")
    print("Let op: als je dit bestand later handmatig aanpast (optie 3),")
    print("worden die wijzigingen overschreven als je opnieuw optie 2 uitvoert.")
    print("--- AUTOMATISCHE BEREKENING AFGEROND ---\n")



def overwrite_settings(outputbestand):
    """Pas handmatig een waarde aan in het outputbestand."""
    print("\n--- INSTELLINGEN AANPASSEN ---")
    print("Je kunt hier een waarde van een systeem handmatig aanpassen.")
    print("Bijvoorbeeld: CV wat lager zetten, ventilatie omhoog of bewatering uitzetten.\n")

    try:
        with open(outputbestand, "r") as f:
            regels = [r.strip() for r in f if r.strip()]
    except FileNotFoundError:
        print(" Outputbestand niet gevonden. Maak het eerst via optie 2 (autoberekenen).")
        return

    if not regels:
        print("  Outputbestand is leeg.")
        return

    # Beschikbare datums tonen
    datums = [regel.split(";")[0] for regel in regels]
    print("Beschikbare datums:")
    for i, d in enumerate(datums, start=1):
        print(f"{i}) {d}")

    keuze = input("\nKies het nummer van de datum die je wilt aanpassen: ").strip()
    if not keuze.isdigit():
        print("  Ongeldige invoer. Voer een nummer in.")
        return

    keuze = int(keuze)
    if keuze < 1 or keuze > len(datums):
        print("  Ongeldig nummer gekozen.")
        return

    datum = datums[keuze - 1]

    # Huidige waarden tonen
    for regel in regels:
        d, cv, vent, water = regel.split(";")
        if d == datum:
            print(f"\nHuidige waarden voor {datum}:")
            print(f"  CV: {cv}%")
            print(f"  Ventilatie: {vent}")
            print(f"  Bewatering: {water}")
            break

    systeem = input("\nSysteem (1=CV, 2=Ventilatie, 3=Bewatering): ").strip()
    if not systeem.isdigit():
        print("  Ongeldige invoer. Gebruik alleen cijfers bij systeem.")
        return

    systeem = int(systeem)

    # Vraag om nieuwe waarde (duidelijk bij bewatering)
    if systeem == 3:
        waarde = input("Nieuwe waarde (typ 'aan' of 'uit'): ").strip()
    else:
        waarde = input("Nieuwe waarde: ").strip()

    gevonden = False
    oude_regel = ""
    nieuwe_regel = ""

    for i, regel in enumerate(regels):
        d, cv, vent, water = regel.split(";")

        if d == datum:
            gevonden = True
            oude_regel = regel

            if systeem == 1:
                try:
                    waarde_int = int(waarde)
                    if 0 <= waarde_int <= 100:
                        cv = f"{waarde_int}"
                    else:
                        print("  Ongeldige waarde voor CV (0-100).")
                        return
                except ValueError:
                    print("  Ongeldige invoer, gebruik een getal.")
                    return


            elif systeem == 2:
                try:
                    waarde_int = int(waarde)
                    if 0 <= waarde_int <= 4:
                        vent = f"{waarde_int}"
                    else:
                        print("  Ongeldige waarde voor ventilatie (0-4).")
                        return
                except ValueError:
                    print("  Ongeldige invoer, gebruik een getal.")
                    return


            elif systeem == 3:

                waarde_lc = waarde.lower()
                if waarde_lc == "aan":
                    water = True

                elif waarde_lc == "uit":
                    water = False
                else:
                    print("  Ongeldige waarde voor bewatering. Typ 'aan' of 'uit'.")
                    return

            else:
                print("  Ongeldig systeemnummer. Kies 1, 2 of 3.")
                return

            nieuwe_regel = f"{d};{cv};{vent};{water}"
            regels[i] = nieuwe_regel
            break

    if not gevonden:
        print("  Datum niet gevonden (onverwachte fout).")
        return

    # Schrijf wijzigingen weg
    with open(outputbestand, "w") as f:
        for regel in regels:
            f.write(regel + "\n")

    # Laat het resultaat zien
    print("\n Waarde is aangepast!")
    print("Oude regel:")
    print(" ", oude_regel)
    print("Nieuwe regel:")
    print(" ", nieuwe_regel)
    print("--- INSTELLINGEN AANGEPAST ---\n")
    return


def toon_huidige_instellingen(outputbestand="output.txt"):
    """Toont de huidige instellingen uit het outputbestand op het scherm, netjes uitgelijnd."""
    print("\n--- HUIDIGE INSTELLINGEN ---")

    try:
        with open(outputbestand, "r") as f:
            regels = [r.strip() for r in f if r.strip()]
    except FileNotFoundError:
        print("  Er is nog geen outputbestand gevonden.")
        print("Voer eerst optie 2 uit om automatische berekeningen te maken.\n")
        return

    if not regels:
        print("Het bestand met instellingen is leeg.\n")
        return

    # Print koptekst
    print(f"{'Datum':<12} {'CV (%)':<8} {'Ventilatie':<12} {'Bewatering':<12}")
    print("-" * 46)

    # Print elke regel mooi uitgelijnd
    for regel in regels:
        try:
            datum, cv, vent, water = regel.split(";")
            print(f"{datum:<12} {cv:<8} {vent:<12} {water:<12}")
        except ValueError:
            print(f"  Ongeldige regel in bestand: {regel}")

    print("-" * 46)
    print("--- EINDE VAN HUIDIGE INSTELLINGEN ---\n")


def smart_app_controller():
    """Hoofdmenu van de Smart App Controller."""
    print("Welkom bij de Smart App Controller!")
    print("Dit programma bestuurt de CV, ventilatie en bewatering op basis van weerdata.\n")
    print("Gebruik dit menu om te zien wat er mogelijk is.\n")

    while True:
        print("====== Smart App Controller ======")
        print("1) Toon aantal dagen (invoerdata)")
        print("2) Automatisch berekenen en opslaan")
        print("3) Handmatig een waarde aanpassen")
        print("4) Toon huidige instellingen")
        print("5) Terug naar Smart App hoofdmenu")
        print("==================================")

        try:
            keuze = int(input("Maak een keuze (1-5): ").strip())
        except ValueError:
            print("  Ongeldige invoer. Vul een getal in tussen 1 en 5.\n")
            continue

        if keuze == 1:
            aantal_dagen("input.txt")
        elif keuze == 2:
            auto_bereken("input.txt", "output.txt")
        elif keuze == 3:
            overwrite_settings("output.txt")
        elif keuze == 4:
            toon_huidige_instellingen("output.txt")
        elif keuze == 5:
            print("\nProgramma wordt afgesloten... Tot de volgende keer! ")
            return
        else:
            print("  Ongeldige keuze. Kies een getal tussen 1 en 5.\n")




# Start het programma
smart_app_controller()
