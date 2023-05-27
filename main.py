import streamlit as st
from ScrapeGetYourGuide import  get_getyourguide_trips
from ScrapeGoogle import get_getyourguide_link
import json

search_query = st.text_input("Enter your search query (Has to be fro getyourguide at the moment")

get_started_button = st.button("Get Started!")

if get_started_button:
    web_links = get_getyourguide_link(search_query)
    st.write("The links found from the web are: ", web_links)
    st.write("getting info ...")

    getyourguide_trips = get_getyourguide_trips(web_links)
    output = json.dumps(getyourguide_trips, indent=5)
    st.write("Showing scraped trips: ")
    st.write(output)
