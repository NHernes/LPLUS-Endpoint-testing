import requests,json
import numpy as np
from threading import Thread

payload = {
    'grant_type': 'password',
    'client_id': "",
    'client_secret': "",
    'username': "",
    'password': ""
}

r = requests.post("https://nx-uni-user-group.lplus-teststudio.de/token", 
    data=payload)
token=json.loads(r.text)["access_token"]

headers={
    "Authorization": "Bearer "+token
}


#Ziehe alle Lizenzen
r = requests.get("https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/licences", 
    headers=headers)
#print(r.raise_for_status)
alle_lizenzen=r.json()

Liste_Lizenzen=[]
for count,eintrag in enumerate(alle_lizenzen):
    Übersicht_Fach=[{"Lizenzname":eintrag["name"]},{"Lizenz-ID":eintrag["id"]},{"Faecher":[]}]
    Liste_Lizenzen.append(Übersicht_Fach)



#Ziehe Alle zugehörigen Fächer
for count,eintrag in enumerate(Liste_Lizenzen):
    lizenz_id=eintrag[1]["Lizenz-ID"]

    r = requests.get(f"https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/licences/{lizenz_id}/subjects", 
        headers=headers)
    #print(r.raise_for_status)
    einzellizenz=r.json()

    for zähler,fach in enumerate(einzellizenz):
        eintrag[2]["Faecher"]+=[{"Fach-ID":fach["id"]}]

#pprint(Liste_Lizenzen)

#Ziehe die Aufgaben-Ids für jedes Fach
for count,eintrag in enumerate(Liste_Lizenzen):
    for count, inhalt in enumerate(eintrag[2]["Faecher"]):
        inhalt["Aufgaben"]=[]

        fach_id=inhalt["Fach-ID"]
        r = requests.get(f"https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/licences/{lizenz_id}/subjects/{fach_id}/questions", 
        headers=headers)
        fachaufgaben=r.json()


        for count,ergebnis in enumerate(fachaufgaben):
            inhalt["Aufgaben"].append([{ergebnis["questionId"]:""}])



#Ziehe die Aufgabentypen für jede Aufgabe
if len(Liste_Lizenzen)<6:
    for count,eintrag in enumerate(Liste_Lizenzen):
        for count, inhalt in enumerate(eintrag[2]["Faecher"]):
            for z in inhalt["Aufgaben"]:
                for key,values in z[0].items():
                    aufgabe=key
                    lizenz=eintrag[1]["Lizenz-ID"]
                    fach=inhalt["Fach-ID"]

                    url=f"https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/licences/{lizenz}/subjects/{fach}/questions/{aufgabe}"
                    r = requests.get(url, headers=headers)
                    stop=r.status_code
                    d=r.json()

                    if stop==500:
                        print(url)

                        #sys.exit()
else:
    pieces = 6
    new_arrays = np.array_split(Liste_Lizenzen, pieces)


    manipulierte_Masterliste=[]

    def threading_aufgabenanalyse(array):
        for count,eintrag in enumerate(array):
            for count, inhalt in enumerate(eintrag[2]["Faecher"]):
                for z in inhalt["Aufgaben"]:
                    for key,values in z[0].items():
                        aufgabe=key
                        lizenz=eintrag[1]["Lizenz-ID"]
                        fach=inhalt["Fach-ID"]

                        url=f"https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/licences/{lizenz}/subjects/{fach}/questions/{aufgabe}"
                        r = requests.get(url, headers=headers)
                        stop=r.status_code
                        d=r.json()

                        if stop==500:
                            z[0][aufgabe]=None
                            #sys.exit()
                        else:
                            z[0][aufgabe]=d["questionKind"]

        manipulierte_Masterliste.append(eintrag)


    threads = []
    for i in range(0,6):
        threads.append(Thread(target=threading_aufgabenanalyse, args=(new_arrays[i],)))
        threads[-1].start()
    for thread in threads:
        thread.join()

liste_final=[]
for i in manipulierte_Masterliste:

    listeneintrag=i.tolist()
    liste_final.append(listeneintrag)

for i in liste_final:
    print(i)
    print("")