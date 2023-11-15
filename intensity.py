import json
import folium
from folium.features import CustomIcon
from math import log10
from geopy.distance import geodesic
from selenium import webdriver
import time
import datetime as dt
#powershell
#pip install folium ; pip install geopy ; pip install selenium
#command prompt
#pip install folium && pip install geopy && pip install selenium

img="C:\\Users\\REI\\Documents\\Programs\\earth_center.png"
color={"1":"#46646E","2":"#1E6EE6","3":"#00C8C8","4":"#FAFA64","5-":"#FFB400","5+":"#FF7800","6-":"#E60000","6+":"#A00000","7":"#960096"}
icon_png = CustomIcon(
    icon_image = img,
    icon_size = (12.5, 12.5),
    icon_anchor = (7, 7),
    popup_anchor = (3, 3)
)

def sum_sindo_map(latitude,longitude,Predicted_latitude, Predicted_longitude,depth,magJMA):
    epicenterLocaltion = [latitude, longitude]
    pointLocaltion = [Predicted_latitude, Predicted_longitude]
    magW = magJMA-0.171
    long = 10**(0.5*magW-1.85)/2
    epicenterDistance = geodesic(epicenterLocaltion, pointLocaltion).km
    hypocenterDistance = (depth**2+epicenterDistance**2)**0.5-long
    x = max(hypocenterDistance, 3)
    gpv600 = 10**(0.58*magW+0.0038*depth-1.29 -
    log10(x+0.0028*(10**(0.5*magW)))-0.002*x)
    arv = 1.0
    pgv400 = gpv600*1.31
    pgv = pgv400*arv
    intensity = 2.68+1.72*log10(pgv)
    if intensity < 0.5:
        earthquake_intensity = "xxx"
        max_intensity = 0
    elif intensity >= 0.5 and intensity < 1.5:
        max_intensity = 1
        earthquake_intensity = color["1"]
    elif intensity >= 1.5 and intensity < 2.5:
        max_intensity = 2
        earthquake_intensity = color["2"]
    elif intensity >= 2.5 and intensity < 3.5:
        max_intensity = 3
        earthquake_intensity = color["3"]
    elif intensity >= 3.5 and intensity < 4.5:
        max_intensity = 4
        earthquake_intensity = color["4"]
    elif intensity >= 4.5 and intensity < 5.0:
        max_intensity = 5
        earthquake_intensity = color["5-"]
    elif intensity >= 5.0 and intensity < 5.5:
        max_intensity = 5.5
        earthquake_intensity = color["5+"]
    elif intensity >= 5.5 and intensity < 6.0:
        max_intensity = 6
        earthquake_intensity = color["6-"]
    elif intensity >= 6.0 and intensity < 6.5:
        max_intensity = 6.5
        earthquake_intensity = color["6+"]
    elif intensity >= 6.5:
        max_intensity = 7
        earthquake_intensity = color["7"]
    return earthquake_intensity,max_intensity,intensity

with open("stations.json","r",encoding="utf-8_sig") as f:
    stations=json.load(f)
    f.close()
map_c = folium.Map([35, 135], zoom_start=5.5)

img="earth_center.png"
icon = CustomIcon(
    icon_image = img,
    icon_size = (12.5, 12.5),
    icon_anchor = (7, 7),
    popup_anchor = (3, 3)
)

#緯度
lat_=33.573
#経度
lon_=136.175
#深さ
depth=30
#マグニチュード
mag=8.4

folium.Marker(
        location = [lat_,lon_],
        popup = f'震源 M{mag}',
        icon = icon
    ).add_to(map_c)

sum_sindo_datas=[]
sum_time_be = dt.datetime.now()
print("==============震度計算開始===============")
for num in range(4371):
    lat=stations["data"][num]["lat"]
    lon=stations["data"][num]["lon"]
    a_now_color,a_max_intensity,a_intensity=sum_sindo_map(lat_,lon_,lat,lon,depth,mag)
    sum_sindo_datas.append(f"北緯:{lat} 東経:{lon} 名称:{stations['data'][num]['name']} 計測:{a_intensity}")
    if a_now_color!="xxx":
        folium.CircleMarker(
            location=[lat,lon],
            radius=10,
            popup=a_intensity,
            color=a_now_color,
            fill=True,
            fill_color=a_now_color,
        ).add_to(map_c)
sum_time = dt.datetime.now() - sum_time_be
print(f"===============震度計算終了===============\n計算時間: {(sum_time.microseconds)/1000}ms")
with open("sum_sindo_datas.txt","w") as f:
    f.write("===============計算結果===============\n")
    f.write(f"計算時間: {(sum_time.microseconds)/1000}ms\n")
    for i in (range(len(sum_sindo_datas))):
        f.write(f"{sum_sindo_datas[i]}\n")

map_c.save("C:\\Users\\REI\\Documents\\Programs\\inten.html")
# browser=webdriver.Chrome()
# browser.maximize_window()
# browser.get("C:\\Users\\REI\\Documents\\Programs\\inten.html")
# time.sleep(20)
# browser.quit()