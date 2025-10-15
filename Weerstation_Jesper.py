def weerstation():

    # functie om graden Celsius naar Fahrenheit te maken
    def fahrenheit(temp_celcius):
        return 32 + 1.8 * temp_celcius

    # functie om gevoelstemperatuur te berekenen
    def gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid):
        return temp_celcius - (luchtvochtigheid/100) * windsnelheid

    # functie om weerrapport te maken
    def weerrapport(temp_celcius, windsnelheid, luchtvochtigheid):
        g = gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid)
        if g < 0 and windsnelheid > 10:
            return "Het is heel koud en het stormt! Verwarming helemaal aan!"
        elif g < 0:
            return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"
        elif g >= 0 and g < 10 and windsnelheid > 12:
            return "Het is best koud en het waait; verwarming aan en roosters dicht!"
        elif g >= 0 and g < 10:
            return "Het is een beetje koud, elektrische kachel op de benedenverdieping aan!"
        elif g >= 10 and g < 22:
            return "Heerlijk weer, niet te koud of te warm."
        else:
            return "Warm! Airco aan!"

    # hoofdprogramma
    temperaturen = []  # lege lijst om alles te bewaren

    for dag in range(1, 8):  # max 7 dagen

        # temperatuur invoeren
        while True: # <-- Aangepast naar loop met break voor correcte afhandeling
            temperatuur = input(f"Wat is op dag {dag} de temperatuur [°C]: ")
            if temperatuur == "":
                print("bye")
                return
            try:
                temperatuur = float(temperatuur)
                break #<-- gaat door naar volgende vraag
            except ValueError:
                print("Ongeldige invoer, voer een geheel getal in.")

        # windsnelheid invoeren
        while True: # <-- Aangepast naar loop
            windsnelheid = input(f"Wat is op dag {dag} de windsnelheid [m/s]: ")
            if windsnelheid == "":
                print("bye")
                return
            try:
                windsnelheid = float(windsnelheid)
                break # <-- gaat door naar volgende vraag
            except ValueError:
                print("Ongeldige invoer, voer een getal in.")

        # luchtvochtigheid invoeren
        while True: # <-- Aangepast naar loop
            luchtvochtigheid = input(f"Wat is op dag {dag} de vochtigheid [%]: ")
            if luchtvochtigheid == "":
                print("bye")
                return
            try:
                luchtvochtigheid = int(luchtvochtigheid)
                if 0 <= luchtvochtigheid <= 100: #laatste vereiste om luchtvochtigheid tussen 0 en 100 te doen. Dit zie ik ook nu pas bij de vereiste.
                    break
                else:
                    print("Voer een waarde in tussen 0 en 100.")
            except ValueError:
                print("Ongeldige invoer, voer een geheel getal in.")

        # temperatuur opslaan voor later gemiddelde in de lege list met append
        temperaturen.append(temperatuur)

        # gemiddelde berekenen
        gemiddelde = sum(temperaturen) / len(temperaturen)

        # print alles
        print("Het is", temperatuur, "C (", fahrenheit(temperatuur), "F)")
        print(weerrapport(temperatuur, windsnelheid, luchtvochtigheid))
        print("Gem. temp tot nu toe is", gemiddelde)
        print("======================================")


def hoofdmenu():
    print("Welkom bij het Weerstation-programma!\n")
    print("Dit programma helpt je om dagelijkse weergegevens in te voeren,")
    print("zoals temperatuur, windsnelheid en luchtvochtigheid,")
    print("en geeft op basis daarvan een passend weerrapport.")
    print("Gebruik het menu hieronder om te beginnen.\n")
    while True:
        print("\n=== Weerstation ===")
        print("1. Weerstation gebruiken")
        print("2. Terug naar Smart App hoofdmenu")
        print("=================")

        try:
            keuze = int(input("Maak een keuze (1-2): ").strip())
        except ValueError:
            print("Ongeldige invoer, voer een getal in (1 of 2).")
            continue

        if keuze == 1:
            weerstation()
        elif keuze == 2:
            print("Programma wordt afgesloten... Tot ziens!")
            return
        else:
            print("Ongeldige keuze, kies 1 of 2.")


# Start het programma
hoofdmenu()

