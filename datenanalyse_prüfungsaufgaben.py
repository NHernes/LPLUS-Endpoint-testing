from distutils.util import change_root
import json,time,sys
import pandas as pd
from json2table import convert

# Opening JSON file
f = open('aufgabendaten_clean.json')
data = json.load(f)


t = open('aufgabendaten_clean_aufgabenanzahl.json')
data_erweitert = json.load(t)
#Wie viele Lizenzen pro FB
def lizenzanalyse():
    fachbereiche={"bcp":0,"erzpsy":0,"vetmed":0,"wiwiss":0,"physik":0,"jfk":0,"geowiss":0,"polsoz":0,"philgeist":0,"sz":0,"rewiss":0,"geschkult":0,"matheinf":0}

    for eintrag in data:
        for key,items in fachbereiche.items():
            if key==eintrag[1]["Fachbereich"]:
                #print(eintrag[1]["Fachbereich"],key)
                anzahl=items
                anzahl+=1
                neuer_eintrag={key:anzahl}
                print(eintrag[0],neuer_eintrag)
                fachbereiche.update(neuer_eintrag)
                break
                #time.sleep(1)

    print(fachbereiche)

#Wie viele Aufgaben durchschnittlich pro Prüfung
def aufgaben_pro_prüfung_generieren():
    for count,i in enumerate(data):
        #print(i[4]["Faecher"],"\n")
        fächer=i[4]["Faecher"]
        

        for count,eintrag in enumerate(fächer):
            zähler=0
            aufgabensammlung=eintrag["Aufgaben"]
            for z in aufgabensammlung:
               # print(z)
                zähler+=1
            k={'Aufgabenanzahl':zähler}
            i[4]["Faecher"][count].update(k)
            #print(i[4]["Faecher"][count])
    print(data)
    
    with open("aufgabendaten_clean_aufgabenanzahl.json","w") as f:
        json.dump(data, f)
    
def aufgaben_pro_fb():
    fachbereiche={"bcp":[0,0,0],"erzpsy":[0,0,0],"vetmed":[0,0,0],"wiwiss":[0,0,0],"physik":[0,0,0],"jfk":[0,0,0],"geowiss":[0,0,0],"polsoz":[0,0,0],"philgeist":[0,0,0],"sz":[0,0,0],"rewiss":[0,0,0],"geschkult":[0,0,0],"matheinf":[0,0,0]}

    for eintrag in data_erweitert:
        fächer=eintrag[4]["Faecher"]
        fb=eintrag[1]["Fachbereich"]
        #print(fächer,fb)

        anzahl_aufgaben_pro_fach=0
        fächer_pro_lizenz=len(fächer)

        anzahl_aufgaben_pro_fach_misc=0
        anzahl_fächer_misc=0

        for items in fächer:
            anzahl_aufgaben_pro_fach=anzahl_aufgaben_pro_fach+items["Aufgabenanzahl"]
        
        schalter=False
        for key,fachbereich in fachbereiche.items():
            
            if fb==key:
                fachbereich[0]=fachbereich[0]+anzahl_aufgaben_pro_fach
                fachbereich[1]=fachbereich[1]+fächer_pro_lizenz
                schalter=True

        if schalter==False:
            anzahl_aufgaben_pro_fach_misc=anzahl_aufgaben_pro_fach_misc+anzahl_aufgaben_pro_fach
            anzahl_fächer_misc=anzahl_fächer_misc+fächer_pro_lizenz
            print(eintrag)

    anzahl_gesamt_aufgaben=0
    for key,fachbereich in fachbereiche.items():
        fachbereich[2]=round((fachbereich[0]/fachbereich[1]),2)
        anzahl_gesamt_aufgaben=anzahl_gesamt_aufgaben+fachbereich[0]

    print(fachbereiche)
    print(anzahl_gesamt_aufgaben)
    print(anzahl_aufgaben_pro_fach_misc,anzahl_fächer_misc)

def aufgabentypen_pro_prüfung():
    aufgabentypen={"MultipleChoice":0,"SpecialAnswer":0,"Cloze":0,"TextOnly":0,"RadioButton":0,"DragDropPicture":0,"DragDropText":0,"MultipleChoiceResponsiveLayout":0,"HotSpotSingle":0,"HotSpotGroup":0,"RadioButtonResponsiveLayout":0}
    zähler_aufgaben=0
    zähler_fächer=0
    for count,i in enumerate(data_erweitert):
        fächer=i[4]["Faecher"]
        

        for count,eintrag in enumerate(fächer):
            zähler_fächer+=1
            aufgabensammlung=eintrag["Aufgaben"]
            

            try:
                for t in aufgabensammlung:
                    for z in t:

                        for key,item in z.items():
                            for key2,item2 in aufgabentypen.items():
                                if item==key2:
                                    zähler_aufgaben+=1
                                    aufgabentypen[key2]+=1

            
            except:
                pass
                #time.sleep(1)
      
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style" : "width:100%"}
    html = convert(aufgabentypen, build_direction=build_direction, table_attributes=table_attributes)
    print(html,"\n\n")      

    print(aufgabentypen)
    print(zähler_aufgaben)
    print(zähler_fächer)

def aufgabentypen_pro_prüfung_pro_semester():
    
    semester_sammlung=["Wintersemester 19/20","Sommersemester 2020","Wintersemester 2020/2021","Sommersemester 2021","Wintersemester 2021/2022","Sommersemester 2022","Wintersemester 2022/2023",None]
    
    #aufgabentypen={"MultipleChoice":0,"SpecialAnswer":0,"Cloze":0,"TextOnly":0,"RadioButton":0,"DragDropPicture":0,"DragDropText":0,"MultipleChoiceResponsiveLayout":0,"HotSpotSingle":0,"HotSpotGroup":0}
    zähler_aufgaben=0
    zähler_fächer=0
    zähler_fächer_semester=0

    for semester in semester_sammlung:
        zähler_fächer_semester=0
        aufgabentypen={"MultipleChoice":0,"SpecialAnswer":0,"Cloze":0,"TextOnly":0,"RadioButton":0,"DragDropPicture":0,"DragDropText":0,"MultipleChoiceResponsiveLayout":0,"HotSpotSingle":0,"HotSpotGroup":0,"RadioButtonResponsiveLayout":0}
        for count,i in enumerate(data_erweitert):
            if i[2]["Semester"]==semester:
                fächer=i[4]["Faecher"]
                

                for count,eintrag in enumerate(fächer):
                    zähler_fächer+=1
                    zähler_fächer_semester+=1
                    aufgabensammlung=eintrag["Aufgaben"]
                    

                    try:
                        for t in aufgabensammlung:
                            for z in t:

                                for key,item in z.items():
                                    for key2,item2 in aufgabentypen.items():
                                        if item==key2:
                                            zähler_aufgaben+=1
                                            aufgabentypen[key2]+=1

                    except:
                        pass
                        #time.sleep(1)

        print(semester, aufgabentypen, zähler_fächer_semester)
        build_direction = "LEFT_TO_RIGHT"
        table_attributes = {"style" : "width:100%"}
        html = convert(aufgabentypen, build_direction=build_direction, table_attributes=table_attributes)
        print(html,"\n\n")

    print(zähler_aufgaben)
    print(zähler_fächer)

def aufgabenanzahl_pro_fb_semester():
    
    semester_sammlung=["Wintersemester 19/20","Sommersemester 2020","Wintersemester 2020/2021","Sommersemester 2021","Wintersemester 2021/2022","Sommersemester 2022","Wintersemester 2022/2023",None]


    for semester in semester_sammlung:
        fachbereiche={"bcp":[0,0,0],"erzpsy":[0,0,0],"vetmed":[0,0,0],"wiwiss":[0,0,0],"physik":[0,0,0],"jfk":[0,0,0],"geowiss":[0,0,0],"polsoz":[0,0,0],"philgeist":[0,0,0],"sz":[0,0,0],"rewiss":[0,0,0],"geschkult":[0,0,0],"matheinf":[0,0,0]}

        for eintrag in data_erweitert:
            if eintrag[2]["Semester"] not in semester_sammlung:
                #print(eintrag)
                pass
                
            if eintrag[2]["Semester"]==semester:
                schalter_c=True
                fächer=eintrag[4]["Faecher"]

                fb=eintrag[1]["Fachbereich"]
                #print(fächer,fb)

                anzahl_aufgaben_pro_fach=0
                fächer_pro_lizenz=len(fächer)

                anzahl_aufgaben_pro_fach_misc=0
                anzahl_fächer_misc=0

                for items in fächer:
                    anzahl_aufgaben_pro_fach=anzahl_aufgaben_pro_fach+items["Aufgabenanzahl"]
                
                schalter=False
                for key,fachbereich in fachbereiche.items():
                    if fb==key:
                        fachbereich[0]=fachbereich[0]+anzahl_aufgaben_pro_fach
                        fachbereich[1]=fachbereich[1]+fächer_pro_lizenz
                        #print(key,fachbereich)
                        schalter=True

                if schalter==False:
                    anzahl_aufgaben_pro_fach_misc=anzahl_aufgaben_pro_fach_misc+anzahl_aufgaben_pro_fach
                    anzahl_fächer_misc=anzahl_fächer_misc+fächer_pro_lizenz
                    #print(eintrag)



            for key,fachbereich in fachbereiche.items():
                if fachbereich[0]!=0:
                    fachbereich[2]=round((fachbereich[0]/fachbereich[1]),2)

        print(semester,fachbereiche)
        print(f"Nicht zuordnenbar: Fächer: {anzahl_fächer_misc}, Aufgaben: {anzahl_aufgaben_pro_fach_misc} \n\n")
        html="""
        <table style="width: 100%;">
        <tbody>
        <tr>
            <td style="width: 25.0000%;"><br></td>
            <td style="width: 25.0000%;">Aufgabenanzahl</td>
            <td style="width: 25.0000%;">F&auml;cher</td>
            <td style="width: 25.0000%;">Ratio</td>
        </tr>"""

        schalter_b=0
        for key,items in fachbereiche.items():
            fachb=f"""
            <tr>
            <td style="width: 25.0000%;">{key}</td>
            <td style="width: 25.0000%;">{items[0]}</td>
            <td style="width: 25.0000%;">{items[1]}</td>
            <td style="width: 25.0000%;">{items[2]}</td>
            </tr>"""
            html=html+fachb
            schalter_b+=1

            if schalter_b==13:
                anzahl_aufgaben_gesamt=0
                anzahl_fächer_gesamt=0
                ratio=0
                for key,items in fachbereiche.items():
                    anzahl_aufgaben_gesamt=anzahl_aufgaben_gesamt+items[0]
                    anzahl_fächer_gesamt=anzahl_fächer_gesamt+items[1]
                ratio=anzahl_aufgaben_gesamt/anzahl_fächer_gesamt
                gesamtübersicht=f"""
                    <tr>
                    <td style="width: 25.0000%;">Gesamt</td>
                    <td style="width: 25.0000%;">{anzahl_aufgaben_gesamt}</td>
                    <td style="width: 25.0000%;">{anzahl_fächer_gesamt}</td>
                    <td style="width: 25.0000%;">{ratio}</td>
                    </tr>
                """
                html=html+gesamtübersicht
                schalter_b=0


        ende="""    
            </tbody>
            </table>
        """
        html=html+ende
        print(html,"\n\n")
        
def freitext_antworten():
    aufgabentypen={"TextOnly":0}
    zähler_fächer=0
    zähler_lizenzen=0
    zähler_freitext_gesamt=0
    zähler_freitext_bepunktet=0
    zähler_freitext_unbepunktet=0

    for count,i in enumerate(data_erweitert):
        schalter_2=False
        fächer=i[4]["Faecher"]
        

        for count,eintrag in enumerate(fächer):
            schalter=False
            for t in eintrag["Aufgaben"]:
                
                for key,items in t[0].items():
                        
                    	if items=="TextOnly":
                            zähler_freitext_gesamt+=1

                            if float(t[1]["Average"])>0:
                                schalter=True
                                schalter_2=True
                                zähler_freitext_bepunktet+=1
                            else:

                                zähler_freitext_unbepunktet+=1

            if schalter:
                zähler_fächer+=1
        if schalter_2:
            zähler_lizenzen+=1
    

    print(f"Freitextaufgaben gesamt: {zähler_freitext_gesamt}, Freitextaufgaben bepunktet: {zähler_freitext_bepunktet}, Freitextaufgaben unbepunktet: {zähler_freitext_unbepunktet}, Fächer mit mindestens einer bepunkteten Freitextaufgabe: {zähler_fächer}, Lizenzen mit mindestens einer bepunkteten Freitextaufgabe: {zähler_lizenzen}")
    print(f"Essay tasks total: {zähler_freitext_gesamt}, essay tasks graded: {zähler_freitext_bepunktet}, essay tasks not graded: {zähler_freitext_unbepunktet}, subjects with at least one graded essay task: {zähler_fächer}, licenses with at least one graded essay task: {zähler_lizenzen}")


freitext_antworten()