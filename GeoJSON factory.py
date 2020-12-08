import geopandas as gpd
import numpy as np
import pandas as pd

mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"


# full_data_path = 'Compressed_Mortality_1999_2016.txt'
# df = pd.read_csv(full_data_path, sep = '\t+', dtype = str)
# df = df.replace('Suppressed', np.nan, regex=True)
#
# df['"County Code"'] = df['"County Code"'].apply(lambda x: x.strip('"'))

dfg = gpd.read_file('us-counties.json',encoding="utf-8")
dfg['id'] = dfg['id'].apply(lambda x: x.zfill(5))

df2 = pd.read_csv('us_counties_covid19_daily.csv',encoding="utf-8")

df2=df2.dropna()
df2['FIPS'] = df2['fips'].apply(lambda x: str(int(x)).zfill(5))
df2['mounth']=df2['date'].apply(lambda x:int(str(x).split("/")[1]))

df2=df2.groupby([df2['mounth'],df2['FIPS']],as_index=False).max()

BINS = [
    "0",
    "1-500",
    "501-1000",
    "1001-1500",
    "1501-2200",
    "2201-3000",
    "3001-4000",
    "4001-5000",
    "5001-6000",
    "6001-7000",
    "7001-8000",
    "8001-9000",
    "9001-10000",
    "10001-11500",
    "11500-13000",
    "-13001",
]

def map_bins(x):
    if x==0:
        return "0"
    elif x in range(1,501):
        return "1-500"
    elif x in range(501,1001):
        return "501-1000"
    elif x in range(1001,1501):
        return "1001-1500"
    elif x in range(1501,2201):
        return "1501-2200"
    elif x in range(2201,3001):
        return "2201-3000"
    elif x in range(3001,4001):
        return "3001-4000"
    elif x in range(4001,5001):
        return "4001-5000"
    elif x in range(5001,6001):
        return "5001-6000"
    elif x in range(6001,7001):
        return "6001-7000"
    elif x in range(7001,8001):
        return "7001-8000"
    elif x in range(8001,9001):
        return "8001-9000"
    elif x in range(9001,10001):
        return "9001-10000"
    elif x in range(10001,11501):
        return "10001-11500"
    elif x in range(11501,13000):
        return "11501-13000"
    elif x >=13001:
        return "-13001"

df2["bins"] = df2["cases"].apply(
    lambda x: map_bins(x)
)



Mounths = range(1,13)

bins = df2['bins'].unique()
for mon in Mounths:
    df_single_mounth = df2[(df2.mounth <= mon)]

    merged = dfg.merge(df_single_mounth, right_on='FIPS', left_on='id' )
    record=[]
    for bin in bins:
        print(mon,bin)
        geo_layer = merged[(merged['bins'] == bin)].drop(['bins','mounth','FIPS'],axis = 1)
        # geo_layer=pd.merge(geo_layer,df3,how = 'right',on='FIPS').fillna(0)
        # try:
        if geo_layer.empty:
            continue
        geo_layer.to_file("{0}/{1}.geojson".format(mon, bin), driver='GeoJSON', encoding="utf-8")
        # except Exception as e:
        #     print('err')
        #     print(e)


