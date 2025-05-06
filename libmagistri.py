#include "smsl.h"

import sys, os

#sys.path = [os.path.join(os.getcwd(), "lib")]

import requests, re

URL = "https://bakaweb.cichnovabrno.cz/api/"

def login(username, password):
    data = {"Content-Type": "application/x-www-form-urlencoded",
            "grant_type": "password",
            "client_id": "ANDR",
            "username": username,
            "password": password
            }
    r = requests.post(URL + "login", data=data)
    return eval(r.content.decode())


def get_marks(access_token):
    data = {"Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + access_token
            }
    r = requests.get(URL + "3/marks", headers=data)
    m =  eval(r.content.decode().replace(":true", ":True").replace(":false", ":False").replace(":null", ":None"))["Subjects"]
    #m = eval(readf("znamky.json").replace(":true", ":True").replace(":false", ":False").replace(":null", ":None"))["Subjects"]
    m_ = {}
    for i in range(len(m)):
        #write("m[i]: " + str(m[i]))
        s_abbrev = m[i]["Subject"]["Abbrev"]
        del m[i]["Subject"]["Id"]
        m_[s_abbrev] = {"subject"        : m[i]["Subject"],
                        "average"        : m[i]["AverageText"],
                        "note"           : m[i]["SubjectNote"],
                        "marks"          : [],
                        "temp_mark"      : "",
                        "temp_mark_note" : ""
                        }
        if m[i]["TemporaryMark"] != "": m_[s_abbrev]["temp_mark"] = m[i]["TemporaryMark"]
        if m[i]["TemporaryMarkNote"] != "": m_[s_abbrev]["temp_mark_note"] = m[i]["TemporaryMarkNote"]
        del m[i]["Subject"]
        del m[i]["AverageText"]
        del m[i]["SubjectNote"]
        del m[i]["PointsOnly"]
        del m[i]["MarkPredictionEnabled"]
        for k in m[i]:
            #print(f"{m[i][k]= }")
            for l in m[i][k]:
                try:
                    #print(f"{l= }")
                    l["MarkDate"] = re.sub(r"T.*", "", l["MarkDate"])
                    l["MarkDate"] = l["MarkDate"].split("-")
                    date_start = ""
                    for j in reversed(l["MarkDate"]):
                        date_start += j
                        if j != l["MarkDate"][0]:date_start += ". "
                    
                    l["MarkDate"] = date_start

                    l["EditDate"] = re.sub(r"T.*", "", l["EditDate"])
                    l["EditDate"] = l["EditDate"].split("-")
                    date_end = ""
                    for j in reversed(l["EditDate"]):
                        date_end += j
                        if j != l["EditDate"][0]:date_end += ". "
                    
                    l["EditDate"] = date_end
                    m_[s_abbrev]["marks"].append(l)
                except Exception as e:
                    pass
            
        
    
    return m_


def get_hw(access_token):
    data = {"Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + access_token
            }
    r = requests.get(URL + "3/homeworks", headers=data)
    hw =  eval(r.content.decode().replace(":true", ":True").replace(":false", ":False"))["Homeworks"]
    
    for i in range(len(hw)):
        hw[i]["DateStart"] = re.sub(r"T.*", "", hw[i]["DateStart"])
        hw[i]["DateStart"] = hw[i]["DateStart"].split("-")
        date_start = ""
        for j in reversed(hw[i]["DateStart"]):
            date_start += j
            if j != hw[i]["DateStart"][0]:date_start += ". "
        
        hw[i]["DateStart"] = date_start
        
        hw[i]["DateEnd"] = re.sub(r"T.*", "", hw[i]["DateEnd"])
        hw[i]["DateEnd"] = hw[i]["DateEnd"].split("-")
        date_end = ""
        for j in reversed(hw[i]["DateEnd"]):
            date_end += j
            if j != hw[i]["DateEnd"][0]:date_end += ". "
        
        hw[i]["DateEnd"] = date_end

        hw_ = []
        for i in hw:
            hw_dict = {"start_date": i["DateStart"],
                       "end_date"   : i["DateEnd"],
                       "contents"   : i["Content"],
                       "done"       : i["Done"],
                       "closed"     : i["Closed"],
                       "class"      : i["Class"]["Abbrev"],
                       "subject"    : i["Subject"]["Name"] + f' ({i["Subject"]["Abbrev"]})',
                       "teacher"    : i["Teacher"]["Name"] + f' ({i["Teacher"]["Abbrev"]})',
                       "finished"   : i["Finished"]
                       }
            hw_.append(hw_dict)
        
    
    return hw_


def get_data(id, dict, type, item="Abbrev"):
    for i in dict[type]:
        if i["Id"] == id:
            if item == None:return i
            else:return i[item]
        
    


def get_ttable(access_token):
    data = {"Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + access_token
            }
    r = requests.get(URL + "3/timetable/actual", headers=data)
    tt =  eval(r.content.decode().replace(":true", ":True").replace(":false", ":False").replace(":null", ":None"))
    tt_dict = {}
    days = ["Po", "Ut", "St", "Ct", "Pa"]
    for i in tt["Days"]:
        a = []
        prev_b = {}
        for j in i["Atoms"]:
            b = {
                 "hour"   : get_data(j["HourId"], tt, "Hours", None),
                 "subject": get_data(j["SubjectId"], tt, "Subjects"),
                 "room"   : get_data(j["RoomId"], tt, "Rooms")
                 }
            try:
                if int(b["hour"]["Caption"]) != int(prev_b["hour"]["Caption"]) + 1:
                    a.append(
                        {"hour": {"Id": 0, "Caption": int(b["hour"]["Caption"]) + 1},
                         "subject": "___",
                         "room"   : "___"
                         })
                
            
            except KeyError:
                pass
            
            a.append(b)
            prev_b = b
        
        tt_dict[days[i["DayOfWeek"]-1]] = a
    
    return tt_dict

#include "smsl.h"

class object(object):
    def __iter__(self):
        return [self].__iter__()
    


class list(list):
    def ____(self, value):
        try:
            return super().__init__(value)
        
        except TypeError:
            return eval(f"[value]", {}) # Přepsat co nejdřive
        
    
    def __init__(self, value):
        return self.____(value)
    
    
    def  __repr__(self):
        repr_str = "{"
        for i in self:
            if i != self[-1]:
                repr_str += str(i) + ", "
            
            else: repr_str += str(i) 
        
        repr_str += "}"
        return repr_str
    

    def e_to_string(self):
        list_ = []
        for i in self:
            list_.append(str(i))
        
        self = list_
        return list_
    


if __import__("os").name == "posix":
    tmp_dir = "/tmp"

else:
    tmp_dir = r"%HOMEDRIVE%\%HOMEPATH%\AppData\Local\Temp\smsl-cache"


def writef(filename, contents, append=False, binary=False):
    mode = "w"
    if append:mode = "a"
    if binary:mode += "b"
    f = open(filename, mode)
    f.write(contents)
    f.close()


def write(value, end="\n", sep=""):
    print(value, end=end, sep=sep)


def readf(filename, binary=False):
    if binary:f = open(filename, "rb")
    else:f = open(filename, "r")
    return f.read()


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
