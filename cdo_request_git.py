import requests
import json
import datetime
import pandas as pd
from pandas import json_normalize
import pprint
#Indiana id= FIPS:18
# name: 'BLOOMINGTON INDIANA UNIVERSITY, IN US','id': 'GHCND:USC00120784',
#dataset: GHCND is two days behind
#looks like you can only run one year at a time. Will need to format string and concat frames
#& datatypeid=SNOW, removed in order to get a full year of data
token = ''
headers = { 'token': token}
baseUrl= r"https://www.ncdc.noaa.gov/cdo-web/api/v2/"
def get_weather(startdate,enddate):

    url = baseUrl + "data?datasetid=GHCND&stationid=GHCND:USC00120784&" \
          "datatypeid=PRCP&datatypeid=TMAX&datatypeid=TMIN&" \
          "units=standard&startdate={}&enddate={}&limit=1000".format(startdate,enddate)
    response=requests.get(url, headers=headers)
    jsonresponse = json.loads(response.text, strict=False)
    #pprint.pprint(jsonresponse)
    weather=json_normalize(jsonresponse['results'])
    weather.drop(columns=['attributes', 'station'], inplace=True)
    df2=weather.pivot(index='date', columns='datatype', values='value')
    df2['date']=pd.to_datetime(df2.index)
    #print(len(df2))
    #df2.to_csv('weather.csv')
    return df2

years=list(range(10,23))
frames=pd.DataFrame()
for i in years:
    i=str(i)
    startdate='20'+i+'-01-01'
    enddate = '20'+i+'-12-31'
    frame=get_weather(startdate,enddate)
    frames=pd.concat([frames,frame])
    print(len(frames))

index=list(range(0,len(frames)-1))
frames.reindex(index)
frames.to_csv('weather_all.csv',index=False)
#response = requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets", headers=headers)
#response = requests.get ("https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationid=FIPS:18&datasetid=GHCND", headers=headers)
#response = requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CITY&sortfield=name&sortorder=asc", headers=headers)
#response= requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:18&datasetid=GHCND", headers=headers)
#response=requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?datasetid=GHCND&locationid=ZIP:47408",
#                      headers=headers)
#response=requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=ZIP:47408&startdate=2022-01-01&enddate=2022-04-04",
#                      headers=headers)
#response=requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/datatypes?stationid=GHCND:USC00120784", headers=headers)