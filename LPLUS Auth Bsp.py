import requests
import json

payload = {
    'grant_type': 'password',
    'client_id': "PublicApi",
    'client_secret': "LTS-RESTfulClient--",
    
    #Hier Credentials eintragen
    'username': "",
    'password': ""
}
#Bei der URL euren Uni Vorsatz eintragen, wenn ihr auf die Live Plattform wollt. Die NX Plattform geht aber auch und eignet sich zum testen.
r = requests.post("https://nx-uni-user-group.lplus-teststudio.de/token", 
    data=payload)
token=json.loads(r.text)["access_token"]

print(token) # Der Token wird dann bei den Requests über den Bearer im Header mitgegeben.