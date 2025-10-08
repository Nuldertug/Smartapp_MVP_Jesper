
import requests
import subprocess


def weerstation():
    try:
        subprocess.run(["python", "Weerstation_Jesper.py"])
    except FileNotFoundError:
        print(" Fout: Weerstation.py niet gevonden.")
    except Exception as e:
        print(f" Er is een fout opgetreden: {e}")

def smart_controller():
    try:
        subprocess.run(["python", "Smart_Controller_Jesper.py"])
    except FileNotFoundError:
        print(" Fout: controller.py niet gevonden.")
    except Exception as e:
        print(f" Er is een fout opgetreden: {e}")


def temperatuur_Utrecht():
    latitude = 52.0907
    longitude = 5.1214
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temperature = data["current"]["temperature_2m"]
        time = data["current"]["time"]
        print(f" De huidige temperatuur in Utrecht is {temperature}°C (gemeten om {time})")

    except Exception as e:
        print(f" Er is een fout opgetreden: {e}")


def Hoofdmenu():

    #Hoofdmenu van app
    print("Welkom bij de Smart Home app! \n")

    while True:
        print("                    ===== Hoofdmenu =====\n")
        print("                 ===== Maak een keuze =====")
        print("1. Weerstation - Toont actuele meetgegevens van het weerstation.")
        print("2. Smart controller -  Stuurt slimme apparaten aan op basis van daggegevens.")
        print("3. Temperatuur Utrecht - Haalt de actuele temperatuur op van Utrecht.")
        print("4. Stoppen")
        print("===============================================================================")

        try:
            keuze = int(input("Maak een keuze (1-4)"))

        except ValueError:
            print("Ongeldige invoer. Voer een getal in van 1 t/m 4. ")
            continue

        if keuze == 1:
            print("\n Weerstation wordt gestart...\n")
            weerstation()

        elif keuze == 2:
            print("\n Smart Controller wordt geopend...\n")
            smart_controller()

        elif keuze == 3:
            print("\n Temperatuur wordt opgehaald...\n")
            temperatuur_Utrecht()

        elif keuze == 4:
            print("Bedankt voor het gebruiken!")
            break
        else:
            print("Ongeldige keuze. Kies een getal van (1 t/m 4). ")

Hoofdmenu()
