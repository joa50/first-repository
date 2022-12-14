import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from math import * 

st.set_page_config(
    page_title="CS230 Final Project-Volcanoes",
    page_icon="volcano_icon.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'mailto:tconnors@bentley.edu',
        'Report a bug': "mailto:jtimm@falcon.bentley.edu",
        'About': "# This is an *extremely* cool app about volcanoes!"
    }
)

"""
Class: CS230--Section 1\n
Name: Joachim Timm\n
Description: My final project on the volcanoes.csv dataset.\n
I pledge that I have completed the programming assignment independently.\n
I have not copied the code from a student or any source.\n
I have not given my code to any student.\n
"""

FILENAME = "volcanoes.csv"
FILE_CITIES = "worldcities.csv"

volcano = pd.read_csv(FILENAME, encoding="ISO-8859-1")
volcano = volcano.fillna("No Data (unchecked)")
volcano = volcano.replace("Uncertain Evidence", "Evidence Uncertain")

cities = pd.read_csv(FILE_CITIES)


# Haversine formula, finds the distance between two points on a globe
def haversine(lat1=0, lon1=0, lat2=0, lon2=0):

    R = 3959.87433
    
    d_lat = radians(lat2-lat1)
    d_lon = radians(lon2-lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    inside = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    hav = 2 * R * asin(sqrt(inside))

    return hav


# Pulls necessary data from dataframes and calculates distance, using only index
def d_between_vol_city(vol, city):

    lat1 = volcano.iloc[vol]["Latitude"]
    lon1 = volcano.iloc[vol]["Longitude"]

    lat2 = cities.iloc[city]["lat"]
    lon2 = cities.iloc[city]["lon"]

    dist = haversine(lat1, lon1, lat2, lon2)

    return dist


# Creates bar chart
def barchart(df):

    colors = ["lightcoral", "indianred", "firebrick", "brown", "maroon", "darkred"]

    fig, ax = plt.subplots()

    x = np.arange(len(df.index))

    ax.bar(x, height=df["num_vol"], color=colors)
    ax.set_title("All Cities with Volcanoes in a 50 Mile Radius")
    ax.set_xticks(x, df["city"], rotation='vertical', fontsize="x-small")
    ax.set_xlabel("Cities")
    ax.set_ylabel("Amount of Volcanoes")

    return fig


def piechart(df, explode=None):

    fig, ax = plt.subplots(figsize=(8, 3))

    labels = df.value_counts("Activity Evidence").index
    sizes = df.value_counts("Activity Evidence").values

    wedges, texts, autotexts = ax.pie(x=sizes, autopct="%1.1f%%", explode=explode)
    ax.legend(wedges, labels, title="Evidence Categories", loc="best")
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title("Activity Evidence")
    ax.axis("equal")

    return fig


# Title
st.title("Volcanic eruptions")
st.markdown("This app analyzes volcanic eruption data throughout the world.")

# sidebar
st.sidebar.title("View Code")
st.sidebar.image("fortnite-volcano.gif")
st.sidebar.write("Here's where you can choose to see the code running this application")

st.image("volcano-scaled.jpg", caption="The Cumbre Vieja Volcano")

# Volcano list and map variable selection
list_options = st.selectbox("Select what portion of the data you'd like to view:", ["Raw Data", "Country", "Primary Volcano Type", "Dominant Rock Type", "Tectonic Setting"])

list_df = pd.DataFrame(columns=volcano.columns)

# Tabs for viewing the list and map
tab_list, tab_map, tab_pie = st.tabs(["Volcano Data", "Volcano Map", "Volcano Pie Chart"])

if list_options != "Raw Data":
    if "Country" in list_options:
        coun_opt = st.multiselect("Select which countries you'd like to see:", volcano.value_counts("Country").index)
        for ele in coun_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Country"] == ele]])

    if "Primary Volcano Type" in list_options:
        pvt_opt = st.multiselect("Select which volcano types you'd like to see:", volcano.value_counts("Primary Volcano Type").index)
        for ele in pvt_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Primary Volcano Type"] == ele]])

    if "Dominant Rock Type" in list_options:
        drt_opt = st.multiselect("Select which rock types you'd like to see:", volcano.value_counts("Dominant Rock Type").index)
        for ele in drt_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Dominant Rock Type"] == ele]])

    if "Tectonic Setting" in list_options:
        tect_opt = st.multiselect("Select which tectonic settings you'd like to see:", volcano.value_counts("Tectonic Setting").index)
        for ele in tect_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Tectonic Setting"] == ele]])
    tab_list.subheader("The More Concise Volcano Dataframe")
    tab_list.write(list_df)
    tab_map.subheader("Map of Volcanoes")
    map_volc = list_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    tab_map.map(map_volc)
    tab_pie.subheader("Pie chart of volcanic eruption activity")
    tab_pie.write("The section Unrest / Holocene means that the volcano is showing unusual activity or is erupting.")
    tab_pie.pyplot(piechart(list_df))
else:
    tab_list.subheader("The DataFrame Containing All Volcanoes")
    tab_list.write(volcano)
    tab_map.subheader("Map of All Volcanoes")
    map_volc = volcano.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    tab_map.map(map_volc)
    tab_pie.subheader("Pie chart of volcanic eruption activity")
    tab_pie.write("The section Unrest / Holocene means that the volcano is showing unusual activity or is erupting.")
    tab_pie.pyplot(piechart(volcano, explode=(0, 0, 0, 0, 0.1, 0)))


# above code
if st.sidebar.checkbox("Show data selection, map, and pie chart code"):
    st.header("The code for the list and map above")
    st.code("""
# Volcano list and map variable selection
list_options = st.selectbox("Select which columns you'd like to choose from for the list and map:", ["Raw Data", "Country", "Primary Volcano Type", "Dominant Rock Type", "Tectonic Setting"])

list_df = pd.DataFrame(columns=volcano.columns)

# Tabs for viewing the list and map
tab_list, tab_map, tab_pie = st.tabs(["Volcano Data", "Volcano Map", "Volcano Pie Chart"])

if list_options != "Raw Data":
    if "Country" in list_options:
        coun_opt = st.multiselect("Select which countries you'd like to see:", volcano.value_counts("Country").index)
        for ele in coun_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Country"] == ele]])

    if "Primary Volcano Type" in list_options:
        pvt_opt = st.multiselect("Select which volcano types you'd like to see:", volcano.value_counts("Primary Volcano Type").index)
        for ele in pvt_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Primary Volcano Type"] == ele]])

    if "Dominant Rock Type" in list_options:
        drt_opt = st.multiselect("Select which rock types you'd like to see:", volcano.value_counts("Dominant Rock Type").index)
        for ele in drt_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Dominant Rock Type"] == ele]])

    if "Tectonic Setting" in list_options:
        tect_opt = st.multiselect("Select which tectonic settings you'd like to see:", volcano.value_counts("Tectonic Setting").index)
        for ele in tect_opt:
            list_df = pd.concat([list_df, volcano.loc[volcano["Tectonic Setting"] == ele]])
    tab_list.subheader("The More Concise Volcano Dataframe")
    tab_list.write(list_df)
    tab_map.subheader("Map of Volcanoes")
    map_volc = list_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    tab_map.map(map_volc)
    tab_pie.subheader("Pie chart of volcanic eruption activity")
    tab_pie.write("The section Unrest / Holocene means that the volcano is showing unusual activity or is erupting.")
    tab_pie.pyplot(piechart(list_df))
else:
    tab_list.subheader("The DataFrame Containing All Volcanoes")
    tab_list.write(volcano)
    tab_map.subheader("Map of All Volcanoes")
    map_volc = volcano.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    tab_map.map(map_volc)
    tab_pie.subheader("Pie chart of volcanic eruption activity")
    tab_pie.write("The section Unrest / Holocene means that the volcano is showing unusual activity or is erupting.")
    tab_pie.pyplot(piechart(volcano, explode=(0, 0, 0, 0, 0.1, 0))
""", language="python")
    
    with st.expander("View Pie Chart Creation Code"):
        st.code("""
def piechart(df, explode=None):

    fig, ax = plt.subplots(figsize=(8, 3))

    labels = df.value_counts("Activity Evidence").index
    sizes = df.value_counts("Activity Evidence").values

    wedges, texts, autotexts = ax.pie(x=sizes, autopct="%1.1f%%", explode=explode)
    ax.legend(wedges, labels, title="Evidence Categories", loc="best")
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title("Activity Evidence")
    ax.axis("equal")

    return fig
        """, language="python")

# cities in proximity of a volcano
vol_city_prox = {}
city_prox_vol_index = []
for city in cities.index:
    count = 0
    temp = volcano[volcano["Country"] == cities.at[city, "country"]]
    for vol in temp.index:
        if d_between_vol_city(vol, city) <= 50:
            city_prox_vol_index.append(vol)
            count += 1
    if count != 0:
        vol_city_prox[city] = count

vol_city_prox_df = pd.DataFrame(list(vol_city_prox.items()), columns=["index", "num_vol"])
vol_city_prox_df.set_index("index", inplace=True)

city_list = [cities.iloc[x]["city_ascii"] for x in vol_city_prox_df.index]
vol_city_prox_df["city"] = city_list

country_list = [cities.iloc[x]["country"] for x in vol_city_prox_df.index]
vol_city_prox_df["Country"] = country_list

vol_city_prox_df = vol_city_prox_df.sort_values("Country", ascending=True)

# bar chart
st.header("Cities within a 50 mile radius of a volcano")
st.write("Using the Harversine formula, I found how many volcanoes are in a 50 mile radius from cities with populations of over 1,000,000.")
st.subheader("Bar Chart")

st.pyplot(barchart(vol_city_prox_df))

# pie chart
st.subheader("Pie Chart")
st.write("The section Unrest / Holocene means that the volcano is showing unusual activity or is erupting.")

city_prox_vol_index_df = volcano.iloc[city_prox_vol_index]

st.pyplot(piechart(city_prox_vol_index_df, explode=(0, 0, 0, 0, 0.1)))

# bar/pie chart code
if st.sidebar.checkbox("Show the code building the DataFrame containing the nearby volcanoes."):
    st.header("The code necessary to building the bar chart above.")
    st.subheader("Haversine Formula Code")
    with st.expander("View Haversine Formula"):
        st.latex(r'''
        d = 2r\arcsin(\sqrt{\sin^2(\frac{\phi_2 - \phi_1}{2}) + \cos(\phi_1)\cos(\phi_2)\sin^2(\frac{\lambda_2 - \lambda_1}{2})})
        ''')
        st.write("Where r = The Earth's radius; φ = Latitude; λ = Longitude")
        st.code("""
# Haversine formula, finds the distance between two points on a globe
def haversine(lat1=0, lon1=0, lat2=0, lon2=0):

    R = 3959.87433
        
    d_lat = radians(lat2-lat1)
    d_lon = radians(lon2-lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    inside = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    hav = 2 * R * asin(sqrt(inside))

    return hav


# Pulls necessary data from dataframes and calculates distance, using only index
def d_between_vol_city(vol, city):

    lat1 = volcano.iloc[vol]["Latitude"]
    lon1 = volcano.iloc[vol]["Longitude"]

    lat2 = cities.iloc[city]["lat"]
    lon2 = cities.iloc[city]["lon"]

    dist = haversine(lat1, lon1, lat2, lon2)

    return dist
        """, language="python")
    
    st.subheader("DataFrame creation code")
    with st.expander("View code"):
        st.code("""
# cities in proximity of a volcano
vol_city_prox = {}
city_prox_vol_index = []
for city in cities.index:
    count = 0
    temp = volcano[volcano["Country"] == cities.at[city, "country"]]
    for vol in temp.index:
        if d_between_vol_city(vol, city) <= 50:
            city_prox_vol_index.append(vol)
            count += 1
    if count != 0:
        vol_city_prox[city] = count

vol_city_prox_df = pd.DataFrame(list(vol_city_prox.items()), columns=["index", "num_vol"])
vol_city_prox_df.set_index("index", inplace=True)

city_list = [cities.iloc[x]["city_ascii"] for x in vol_city_prox_df.index]
vol_city_prox_df["city"] = city_list

country_list = [cities.iloc[x]["country"] for x in vol_city_prox_df.index]
vol_city_prox_df["Country"] = country_list

vol_city_prox_df = vol_city_prox_df.sort_values("Country", ascending=True)
        """, language="python")
    
    st.subheader("Bar chart creation code")
    with st.expander("View Code"):
        st.code("""
# Creates bar chart
def barchart(df):

    colors = ["lightcoral", "indianred", "firebrick", "brown", "maroon", "darkred"]

    fig, ax = plt.subplots()

    x = np.arange(len(df.index))

    ax.bar(x, height=df["num_vol"], color=colors)
    ax.set_title("All Cities with Volcanoes in a 50 Mile Radius")
    ax.set_xticks(x, df["city"], rotation='vertical', fontsize="x-small")
    ax.set_xlabel("Cities")
    ax.set_ylabel("Amount of Volcanoes")

    return fig

st.pyplot(barchart(vol_city_prox_df))

        """, language="python")

    st.subheader("Pie chart code")
    with st.expander("View Code"):
        st.code("""
st.subheader("Pie Chart")
st.write("The section Unrest / Holocene means that the volcano is showing unusual activity or is erupting.")

city_prox_vol_index_df = volcano.iloc[city_prox_vol_index]

st.pyplot(piechart(city_prox_vol_index_df, explode=(0, 0, 0, 0, 0.1)))
        """, language="python")

st.header("The End")
st.success("You've reached the end! Thank you for looking through my application!")
st.image("lalo-wink.gif")
