import requests
import simplejson as json
import pandas as pd

# Retrieve Authentication token from User
headerInfo = {'content-type': 'application/json'}
payload1 = {'username': 'ala@naturemapr.org', 'password': 'BlackMountain1#'}
jLoad = json.dumps(payload1)
ret = requests.post('https://api.naturemapr.org/api/users/authenticate', headers=headerInfo, data=jLoad)

# find start of token
pos1 = ret.text.find('"token":"')
# find end of token
pos2 = ret.text.find('","roles')
#Token starts at pos1 + 9
tStart = pos1 + 9
token = ret.text[tStart:pos2]

# Build Authentication Header parameter
authStr = 'Bearer ' + token
headerT = {'content-type': 'application/json', 'Authorization': authStr}

# sUrl = 'https://api.naturemapr.org/api/sightings?viewMode=Detail&pageNumber=1&pageSize=100'
# res1 = requests.get(sUrl, headers=headerT)
# res = requests.get('https://api.naturemapr.org/api/sightings?viewMode=Detail&pageNumber=1&pageSize=100', headers=headerT)

result_arr = []
# for index in range(1, 100):
rList = []

for index in range(1, 2):
    pageNo = index
    sUrl = 'https://api.naturemapr.org/api/sightings?viewMode=Detail&pageNumber=' + str(pageNo) + '&pageSize=100'
    result = requests.get(sUrl, headers=headerT)
    result_arr.append(result.text)
    rList.append(json.loads(result.text))

#initialise first array to csv with header
df = pd.DataFrame(rList[0])
# Rename data columns
df = df.rename(columns=
{'sightingId':'catalogNumber',
'speciesId':'taxonID',
'category2Title':'taxonRemarks' ,
'scientificName':'scientificName' ,
'commonName':'vernacularName',
'latitude':'decimalLatitude',
'longitude':'decimalLongitude',
'abundanceDescription':'individualCount',
'descriptionPublic':'occurrenceRemarks',
'make':'deviceName',
'lastConfirmedByUsername':'identifiedBy',
'model':'deviceSpecification',
'os': 'deviceOperatingSystem',
'username':'recordedBy',
'lastConfirmedByUsername':'identifiedBy',
'altitude':'verbatimElevation'
})
df.to_csv(r'sightings-1-16000.csv', mode='a',index=False)

for i in range(1,len(rList)):
    df = pd.DataFrame(rList[i])
    df.to_csv(r'sightings-1-16000.csv', mode='a', index=False, header=False)  # append without header

