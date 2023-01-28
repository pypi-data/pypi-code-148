import requests
from rich import print

# kimya v0.0.1

def showpHScale():
    print("[b][red3]0 1 2 3 4 5 6 [/red3][green3]7 [/green3][dodger_blue3]8 9 10 11 12 13 14[/dodger_blue3][/b]")
    print("Acidic     Neutral        Alkaline")

def pH(value):
    if type(value) is int or float:
        if value >= 0 and value <= 6.9:
            print("Acidic")
        elif value == 7:
            print("Neutral")
        elif value >= 7.1 and value <= 14:
            print("Alkaline")
    else:
        raise TypeError("The value parameter is not an int or a float number.")


def calcPressure(force, area) -> float:
    if type(force) and type(area) is int or float:
        p = force / area
        return p
    else:
        raise TypeError("The force or area parameter is not an int or a float number.")

def CtoF(celsius) -> float:
    if type(celsius) is int or float:
        fahrenheit = celsius * 1.8 + 32
        return fahrenheit
    else:
        raise TypeError("The celsius parameter is not an int or a float number.")

def FtoC(fahrenheit) -> float:
    if type(fahrenheit) is int or float:
        celsius = (fahrenheit - 32) / 1.8
        return celsius
    else:
        raise TypeError("The fahrenheit parameter is not an int or a float number.")

def getElement(atomicNumber: int, property):
    r = requests.get("https://neelpatel05.pythonanywhere.com/element/atomicnumber?atomicnumber=" + str(atomicNumber))
    data = r.json()
    if type(atomicNumber) == int:
        if atomicNumber > 0 and atomicNumber <= 118:
            if property == "atomicmass":
                return data["atomicMass"]
            elif property == "atomicradius":
                return data["atomicRadius"]
            elif property == "boilingpoint":
                return data["boilingPoint"]
            elif property == "bondingtype":
                return data["bondingType"]
            elif property == "density":
                return data["density"]
            elif property == "electronaffinity":
                return data["electronAffinity"]
            elif property == "electronegativity":
                return data["electronegativity"]
            elif property == "electronicconfiguration":
                return data["electronicConfiguration"]
            elif property == "groupblock":
                return data["groupBlock"]
            elif property == "ionradius":
                return data["ionRadius"]
            elif property == "ionizationenergy":
                return data["ionizationEnergy"]
            elif property == "meltingpoint":
                return data["meltingPoint"]
            elif property == "name":
                return data["name"]
            elif property == "oxidationstates":
                return data["oxidationStates"]
            elif property == "standardstate":
                return data["standardState"]
            elif property == "symbol":
                return data["symbol"]
            elif property == "vanderwaalsradius":
                return data["vanDerWaalsRadius"]
            elif property == "yeardiscovered":
                return data["yearDiscovered"]
            else:
                raise Exception("Unknown Properity.")

        else:
            raise ValueError("The atomicNumber parameter cannot be negative or greater than 118.")
    else:
        raise TypeError("The atomicNumber parameter is not an int.")