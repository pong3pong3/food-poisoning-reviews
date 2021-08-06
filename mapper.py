import pickle
import folium
with open('food_poison_map.pk','rb') as file:
    food_poison = pickle.load(file)
def paint(x):
    if x==1:
        return 'darkred'
    elif x==2:
        return 'red'
    elif x==3:
        return 'purple'
    elif x==4:
        return 'blue'
    else:
        return 'darkblue'
food_poison.reviews = food_poison.reviews.iloc[-1::-1]
food_poison.reviews.index = reversed(food_poison.reviews.index)
food_poison_map = folium.Map(location = [food_poison.y, food_poison.x])
for i in range(len(food_poison.reviews)):
    layer = folium.FeatureGroup(name = 'Reviewer #'+str(i+1), show = False)
    folium.Marker([food_poison.y, food_poison.x],
                  tooltip = '별점 '+str(food_poison.reviews.loc[i,'point']),
                  popup = folium.Popup(food_poison.reviews.loc[i,'date']+' '+\
                                       food_poison.reviews.loc[i,'contents']+\
                                       ' | '+food_poison.address,
                                       min_width=200, max_width=200)
                  ).add_to(layer)
    footprint = food_poison.footprint[food_poison.reviews.loc[i,'kakaoMapUserId']]
    for j in range(len(footprint)):
        try:
            folium.CircleMarker([footprint.loc[j,'y'], footprint.loc[j,'x']],
                                fill_color = paint(footprint.loc[j,'star']),
                                fill_opacity = .5, weight = 0,
                                tooltip = footprint.loc[j,'name'],
                                popup = folium.Popup(footprint.loc[j,'date'].\
                                                     split(' ')[0]+' '+\
                                                     footprint.loc[j,'contents']+\
                                                     ' | '+footprint.loc[j,'address'],
                                                     min_width=200, max_width=200)
                                ).add_to(layer)
        except:
            continue
    layer.add_to(food_poison_map)
folium.LayerControl(position = 'bottomleft').add_to(food_poison_map)
food_poison_map.save('index.html')
