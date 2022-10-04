#You have to install some modules first, I recommend installing pip. Then you can install all modules via cli
import requests #https://pypi.org/project/requests/
import json #already integrated in python

#Token Handshake
payload = {
    'grant_type': 'password',
    'client_id': "PublicApi",
    'client_secret': "LTS-RESTfulClient--",
    'username': "", #Put your username here
    'password': "" #Put your password here
}

#Get a access token from LPLUS --> important: the access token and credentials are bound to the plattform. In this case: nx-uni-user-group
r = requests.post("https://nx-uni-user-group.lplus-teststudio.de/token", 
    data=payload)

token=json.loads(r.text)["access_token"] #Access the token from the response

print(token)

#Include the token into the https header
headers={
    "Authorization": f"Bearer {token}"
}

#Example 1: Get all users
url= "https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/candidates"
r = requests.get(url, headers=headers)

data=r.json() #Put reponse into json format
print(data)

#Example 2: Get all users for speficic license
licence=78
r = requests.get(f"https://nx-uni-user-group.lplus-teststudio.de/publicapi/v1/licences/{licence}/candidateRelations", headers=headers)

data=r.json() #Put reponse into json format
print(data)
