from libmagistri import *
from getpass import getpass
from predvidac import Predvidac

def read(prompt, type=str, split=False, split_char=" "):
    input_ = input(prompt)
    if split:
        input_ = input_.split(split_char)
        for i in range(len(input_)):
            input_[i] = type(input[i])
        
        return input_
    
    else:return type(input_)


def exit(text=""):
    raise SystemExit(text)

def write(text, end="\n", sep=""):
    print(text, end=end, sep=sep)
#include "builtins.smsl"


#include "libmagistri.smsl"

username = read("Zadej přihlašovací jméno: ")
password = getpass("Zadej heslo: ")
a = login(username, password)
try:
    znamky = get_marks(a["access_token"])
    ukoly = get_hw(a["access_token"])
    rozvrh = get_ttable(a["access_token"])

except KeyError as e: exit("Nesprávné přihlašovací jméno nebo heslo.")

write("Vítej v programu Magistři.")
write("Napiš 'help', 'napoveda' nebo 'pomoc' pro zobrazení nápovědy.")
while True:
    try:
        command = read("(magistri) ")
    except KeyboardInterrupt:
        continue
    except EOFError:
        exit()
    if command in ["help", "napoveda", "pomoc"]:
        write("Seznam příkazů: ")
        write("znamky - Vypíše známky.")
        write("ukoly - Vypíše domácí úkoly.")
        write("rozvrh - Vypíše rozvrh pro tento týden.")
        write("predvidac <predmet> - Otevře předvídač známek.")
        write("exit, ukoncit, konec - Ukončí tento program.")
    
    elif command == "znamky":
        if len(znamky) != 0:
                for i, j in znamky.items():
                    if j["average"] == None:
                        j["average"] = ""
                    write(j["subject"]["Name"])
                    write("\nPrůměr: " + j["average"])
                    for k in j["marks"]:
                        write("Datum: " + k["MarkDate"])
                        write("Datum úpravy: " + k["EditDate"])
                        write(k["Caption"])
                        write("Známka: ", k["MarkText"] + "\n")
                        write("Váha: " + str(k["Weight"]))
                        if k["TypeNote"] != None:
                            write("Druh: " + k["TypeNote"])
                        
                        write("\n")
                    
                    write("\n")
                
            
        
        else:
            write("Vypadá to, že tady nic není.")
        
    
    elif command == "ukoly":
        if len(ukoly) != 0:
            for i in ukoly:
                write("Od: " + i["start_date"])
                write("Do: " + i["end_date"])
                write("Třída: " + i["class"])
                write("Předmět: " + i["subject"])
                write("Učitel: " + i["teacher"])
                write(i["contents"])
                write("Hotovo: ", end="")
                if i["finished"]: write("Ano")
                else: write("Ne")
                write("\n")
            
        
        else:write("Vypadá to, že tady nic není.")
    
    elif command == "rozvrh":
        for i in rozvrh:
            write(i + " ", " ")
            for k in range(2):
                #write(k)
                if k == 1: write("  ", "  ")
                for j in rozvrh[i]:
                    if j["subject"] == None:
                        start = "  "
                        end = "  "
                        j["subject"] = ""
                    elif len(j["subject"]) == 1:
                        start = " "
                        end = "  "
                    
                    else:
                        start = ""
                        if len(j["subject"]) >= 3:
                            end = " "
                            if len(j["subject"]) == 4:
                                subject = list(j["subject"])
                                del subject[-1]
                                j["subject"] = "".join(subject)
                            
                        
                        else: end = "  "

                    if j["room"] == None:
                        j["room"] = "  "
                    elif len(j["room"]) == 4:
                        room = list(j["room"])
                        del room[-1]
                        j["room"] = "".join(room)
                    
                    if k == 0:write(start + j["subject"], end)
                    else:write(j["room"], " ")
                
                write("")
    elif command.startswith("predvidac"):
        __import__("os").system("clear")
        predmet = command.split()[1]
        predmet += " " * (4 - len(predmet))
        print(predmet, znamky.keys())
        if predmet not in znamky.keys():
            print("Neplatný předmět.")
            continue
        znamky2 = [int(x["MarkText"]) for x in znamky[predmet]["marks"]]
        vahy = [int(x["Weight"]) for x in znamky[predmet]["marks"]]
        p = Predvidac(znamky2, vahy)
        try:
            p.spustit()
        except SystemExit:
            pass
    
    elif command in ["exit", "quit", "ukoncit", "zavrit"]:
        exit()
    
    else:write("Neznámý příkaz")

