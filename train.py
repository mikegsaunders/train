import streamlit as st
from streamlit_float import *
import os
import requests
from datetime import datetime

# CRS codes
edinburgh = "EDB"
gala = "GAL"
tweedbank = "TWB"
auth = os.environ.get("TRAIN_API")

headers = {
    "User-Agent": "",
    "x-apikey": auth,
}

baseurl = "https://api1.raildata.org.uk/1010-live-arrival-and-departure-boards-arr-and-dep1_1/LDBWS/api/20220120/GetArrivalDepartureBoard"

# GAL > EDB
url = f"{baseurl}/GAL"
params = {
    "numRows": 10,
    "filterType": "to",
    "filterCrs": "EDB",
    "timeOffset": 0,
    "timeWindow": 120,
}
ge = requests.get(url, params=params, headers=headers)

# EDB > GAL
url = f"{baseurl}/EDB"
params = {
    "numRows": 10,
    "filterType": "to",
    "filterCrs": "GAL",
    "timeOffset": 0,
    "timeWindow": 120,
}
eg = requests.get(url, params=params, headers=headers)

# GAL > TWB
url = f"{baseurl}/GAL"
params = {
    "numRows": 10,
    "filterType": "from",
    "filterCrs": "EDB",
    "timeOffset": 0,
    "timeWindow": 120,
}
gt = requests.get(url, params=params, headers=headers)

# TWB > GAL
url = f"{baseurl}/TWB"
params = {
    "numRows": 10,
    "filterType": "to",
    "filterCrs": "GAL",
    "timeOffset": 0,
    "timeWindow": 120,
}
tg = requests.get(url, params=params, headers=headers)


def time_diff(time1, time2):
    time1 = datetime.strptime(time1, "%H:%M")
    time2 = datetime.strptime(time2, "%H:%M")
    diff = time2 - time1
    mins = int(diff.total_seconds() // 60)
    return mins


def timetable(results, dest):
    for each in results["trainServices"]:
        if each["destination"][0]["crs"] == dest:
            with st.container(border=True):
                if each["isCancelled"] == True:
                    st.write(":red[Cancelled]")
                if each["etd"] != "On time":
                    st.write(
                        f':red[{each["etd"]}] (+{time_diff(each["std"], each["etd"])})'
                    )
                else:
                    st.write(f':green[{each["std"]}]')
                st.write(f'Platform {each.get("platform", "-")}')


col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.expander("**GAL > EDB**", expanded=True):
        results = ge.json()
        dest = "EDB"
        timetable(results, dest)
with col2:
    with st.expander("**EDB > GAL**", expanded=True):
        results = eg.json()
        dest = "TWB"
        timetable(results, dest)
with col3:
    with st.expander("**GAL > TWB**", expanded=True):
        results = gt.json()
        dest = "TWB"
        timetable(results, dest)
with col4:
    with st.expander("**TWB > GAL**", expanded=True):
        results = tg.json()
        dest = "EDB"
        timetable(results, dest)

float_init()
button_container = st.container()
with button_container:
    if st.button(":material/refresh:"):
        st.rerun()
button_css = float_css_helper(left="2rem", bottom="2rem", transition=0)
# Float button container
button_container.float(button_css)
