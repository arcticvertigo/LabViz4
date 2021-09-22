import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
from functools import wraps
import streamlit.components.v1 as components

 
dfo = pd.DataFrame({
'first column': ["Uber pickups in NYC", 'NY trips data'],
})

 
option = st.sidebar.selectbox('Which dataset would you like to study?',dfo['first column'])
 

if option == "Uber pickups in NYC":
    st.title('Uber pickups in NYC')
    filename = r"uber-raw-data-apr14.csv"
    DATE_COLUMN = 'date/time'
else:
    st.title('NY trips data')
    filename = r"ny-trips-data.csv"
    DATE_COLUMN = "tpep_pickup_datetime"





@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_csv(filename, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text(" ")
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)



def count_rows(rows): 
    return len(rows)




def log_time(func):
    def wrapper(*args,**kwargs):

        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        timeTaken = end - start



        d = open("map-uber.txt", 'a')
        d.write("It took "+ str(timeTaken)+" seconds \n\n")

        d.close()
    return wrapper



@log_time
def mapping_data(dataset):

    f = open("map-uber.txt", 'w')
    f.write("")


    d = open("map-uber.txt", 'a')
    
    d.write("Map function\n")

    d.close()

    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = dataset[dataset[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)
    


@log_time
def heat_m(grouped_data):
    d = open("map-uber.txt", 'a')
    d.write("Heatmap function\n")

    d.close()
    fig, ax = plt.subplots()
    sns.heatmap(grouped_data, center=0)
    st.write(fig)


def get_dom(dt): 
    return dt.day 

def get_hour(dat): 
    return dat.hour

def get_min(dt): 
    return dt.minute


def toTime(dataset, col):
    dataset[col]= pd.to_datetime(dataset[col])





if option == "Uber pickups in NYC":

    
    mapping_data(data)


    #data1["Date/Time"]= pd.to_datetime(data1["Date/Time"])
    toTime(data,"date/time")
    #st.write(data1)


    data['day']=data['date/time'].map(get_dom)

    data['hour']= data['date/time'].map(get_hour)



    v = data.groupby(data['day']).apply(count_rows)
    v.sort_values()
    #st.bar_chart(v)
    #st.line_chart(v)
    st.area_chart(v)


    v1 = data.groupby(['day','hour']).apply(count_rows).unstack()


    st.subheader('Heatmap according to the hours and days of the uber pickups')
    heat_m(v1)


    #static component :


    components.iframe("https://blogs.mathworks.com/images/loren/2016/uberNYC_09.png", height=600)

    

else:

    df_new = data.rename(columns={'pickup_latitude': 'lat', 'pickup_longitude': 'longitude'})

    mapping_data(df_new)


    toTime(data, "tpep_pickup_datetime")

    toTime(data, "tpep_dropoff_datetime")


    data['hour']=data['tpep_pickup_datetime'].map(get_hour)


    data['min']=data['tpep_dropoff_datetime'].map(get_min)

    v2 = data.groupby(['hour','min']).apply(count_rows).unstack()

    st.subheader('Heatmap according to the hours and minutes of the NY pickups flights')
    
    heat_m(v2)

    #static component :

    components.iframe("https://www.researchgate.net/profile/Joseph-Chow-3/publication/304498622/figure/fig6/AS:391017745403914@1470237303530/A-comparison-of-the-number-of-trips-and-passengers-in-NY-and-Manhattan.png", height=600)
    
    







