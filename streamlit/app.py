### KICKOFF - CODING AN APP IN STREAMLIT

### import libraries
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import pydeck as pdk
from streamlit_modal import Modal
# import folium
import joblib
modal = Modal(key="Demo Key",title="test")
items = [
    {
        'name': 'Mimoglad Office Chair',
        'price': 22, 
        'description': 'High Back Ergonomic Desk Chair with Adjustable Lumbar Support and Headrest', 
        'image': 'https://m.media-amazon.com/images/I/816aZ0RHypL._AC_SX679_.jpg',
        'declared_handling_days': 3, 
        'shipping_fee': 8,
        'weight': 1, 
        'package_size':3, 
        'distance': 909
        },
    {
        'name': 'LED Lights Room Decor',
        'price': 12, 
        'description': '20m Led Lights Strip for Bedroom Decoration Smart Color Changing Rope Lights SMD 5050 RGB', 
        'image': 'https://m.media-amazon.com/images/I/81H5eeMcvDL._AC_SX679_.jpg',
        'declared_handling_days': 2, 
        'shipping_fee': 0,
        'weight': 1, 
        'package_size':2, 
        'distance': 1500},
        
    {
        'name': 'Corsair HS65 Gaming Headset', 
        'price': 19, 
        'description': 'Dolby Audio 7.1 Surround Sound on PC and Mac, SonarWorks SoundID Technology', 
        'image': 'https://m.media-amazon.com/images/I/913Y8y1f8IL._AC_SX679_.jpg',
        'declared_handling_days': 6, 
        'shipping_fee': 4,
        'weight': 7, 
        'package_size':3, 
        'distance': 134
        },
        {
        'name': 'SereneLife Portable Electric Air',
        'price': 15, 
        'description': '900W 8000 BTU Power Plug-in AC Cold Indoor Room Conditioning System with Cooler', 
        'image': 'https://m.media-amazon.com/images/I/61wSbl1vHBL._AC_SX679_.jpg',
        'declared_handling_days': 2, 
        'shipping_fee': 3,
        'weight': 1, 
        'package_size':3, 
        'distance': 1032
        },
    {
        'name': 'Keurig K-Express',
        'price': 8, 
        'description': 'Single Serve K-Cup Pod Coffee Maker, With A Removable Reservoir', 
        'image': 'https://m.media-amazon.com/images/I/71kP6ZQyMmL._AC_SL1500_.jpg',
        'declared_handling_days': 4, 
        'shipping_fee': 5,
        'weight': 1, 
        'package_size':2, 
        'distance': 671},
        
    {
        'name': 'Melissa & Doug Freestanding ', 
        'price': 14, 
        'description': 'Wooden Fresh Mart Grocery Store | Supermarket Pretend Play, Kids Play Store, Toy Food Stand For Toddlers And Kids Ages 3+', 
        'image': 'https://m.media-amazon.com/images/I/712wUiYitBL._AC_SL1500_.jpg',
        'declared_handling_days': 6, 
        'shipping_fee': 3,
        'weight': 7, 
        'package_size':3, 
        'distance': 236
        },
        {
        'name': '40Pcs Kids Market Playset',
        'price': 9, 
        'description': '2 in 1 Grocery Shop Pretend Play Toy with Cash Register & Shopping Cart', 
        'image': 'https://m.media-amazon.com/images/I/71xiS2Vsk-L._AC_SL1500_.jpg',
        'declared_handling_days': 5, 
        'shipping_fee': 5,
        'weight': 1, 
        'package_size':3, 
        'distance': 579
        },
    {
        'name': 'Little Tikes',
        'price': 7, 
        'description': 'Light-Up 3-foot Trampoline with Folding Handle for Kids Ages 3 to 6', 
        'image': 'https://m.media-amazon.com/images/I/A1uD0uJpgBL._AC_SL1500_.jpg',
        'declared_handling_days': 2, 
        'shipping_fee': 4,
        'weight': 1, 
        'package_size':2, 
        'distance': 685},
        
    {
        'name': 'Besign Adjustable Laptop Table', 
        'price': 9, 
        'description': 'Portable Standing Bed Desk, Notebook Computer Stand for Reading and Writing', 
        'image': 'https://m.media-amazon.com/images/I/612TG3S+upL._AC_SL1001_.jpg',
        'declared_handling_days': 3, 
        'shipping_fee': 4,
        'weight': 7, 
        'package_size':3, 
        'distance': 249
        }
]
st.header('BrainStation Data Science Diploma Capstone Project')
st.subheader("Predict delivery time for online shopping")
st.write('Huy Hoang Vuong')


### To position text and color, you can use html syntax
#st.markdown("<h1 style='text-align: center; color: blue;'>The Final Morning Kick Off </h1>", unsafe_allow_html=True)


#######################################################################################################################################
### DATA LOADING

### A. define function to load data
@st.cache_data # <- add decorators after tried running the load multiple times
def load_data(path, num_rows):

    df = pd.read_csv(path, nrows=num_rows, index_col=0)

    # Streamlit will only recognize 'latitude' or 'lat', 'longitude' or 'lon', as coordinates

    df = df.rename(columns={'buyyer_lat': 'lat', 'buyyer_lon': 'lon'})     
    # df['Start Time'] = pd.to_datetime(df['Start Time'])      # reset dtype for column
     
    return df

### B. Load first 50K rows
df = load_data("Ebay_cleaned.csv", 100000)

### C. Display the dataframe in the app
st.dataframe(df)


#######################################################################################################################################
### STATION MAP
lat1, lon1 = df['lat'], df['lon']  # Coordinates 1
lat2, lon2 = df['seller_lat'], df['seller_lon']    # Coordinates 2

# st.map([[lat1, lon1], [lat2, lon2]])
# # Create a map object
# map = folium.Map(location=[lat1, lon1], zoom_start=12)

# # Add markers for the coordinates
# folium.Marker([lat1, lon1], popup='Location 1').add_to(map)
# folium.Marker([lat2, lon2], popup='Location 2').add_to(map)

# Render the map in Streamlit

st.subheader('Buyer Location')      

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=2,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df[['lat', 'lon']],
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df[['lat', 'lon']],
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))


#######################################################################################################################################
### DATA ANALYSIS & VISUALIZATION

### A. Add a bar chart of usage per hour

st.subheader("Business type")
st.markdown('0: C2C - 1: B2C')
counts = df["b2c_c2c"].value_counts()
st.bar_chart(counts)

#######################################################################################################################################
### MODEL INFERENCE

st.subheader("Using pretrained models to predict delivery date for order")

# A. Load the model using joblib
model = joblib.load('nn_model.pkl')

st.sidebar.subheader("Usage filters")
b2c = st.sidebar.radio('B2C or C2C business', ('B2C', 'C2C'))

delivery = st.sidebar.radio('Delivery type', ('Regular', 'Express', 'Slow'))

# b2c = st.sidebar.checkbox('B2C business')
# b2c = st.sidebar.checkbox('B2C business')
# b2c = st.sidebar.checkbox('B2C business')
# b2c = st.sidebar.checkbox('B2C business')
deliver=0
if delivery == 'Regular': 
    deliver=1
elif delivery== 'Express':
    deliver=2
else:
    deliver=0
if b2c=='B2C':
    business=1
else:
    business=0
current_date= datetime.now()

col_count = 3  # Number of columns
row_count = len(items) // col_count

for i in range(row_count):
    
    row_items = items[i * col_count: (i + 1) * col_count]
    row = st.columns(col_count)

    for j, item in enumerate(row_items):
        with row[j]:
            feature= [business, item['declared_handling_days'], deliver, item['shipping_fee'],item['price'], item['weight'], item['package_size'], item['distance']]
            predict= model.predict([feature])
            date= current_date+ timedelta(days=int(np.round(predict)[0][0]))
            date= date.strftime("%Y-%m-%d" )
            st.image(item['image'], use_column_width=True, caption=item['name'])
            st.markdown(f"**{item['name']}**")
            st.write(item['description'])
            if st.button(f'Buy Now', key=item['name']):
                # Handle the button click
                st.write(f"Buy {item['name']} today and get it before {date} !")
                