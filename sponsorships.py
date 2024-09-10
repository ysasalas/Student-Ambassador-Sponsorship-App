import folium
import pandas as pd
import streamlit as st
import streamlit_folium as st_folium
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Student Ambassador Sponsorship Outreach Hub",
    page_icon=":comet:"
)

st.title(":comet: Student Ambassador Sponsorship Outreach Hub")

st.subheader("Discover and Explore Sponsorship Outreach with Ease")

st.markdown(
"""
Welcome to our platform dedicated to managing sponsorships, locations, and assignments. This site is designed to provide you with comprehensive access to:

- **Sponsorship List:** Explore detailed lists of current sponsorships and their associated details
- **Locations Map:** View information about various sponsor locations to help you navigate effectively
- **Sponsorship Assignments:** Stay updated on assignments, responsibilities, and schedules related to sponsorships

We're committed to making your sponsorship experience straightforward and insightful. Feel free to explore and utilize the tools available here to maximize your engagement and impact.
"""
)

with st.sidebar:
    st.header("Documents & Resources:")
    url_spreadsheet = "https://docs.google.com/spreadsheets/d/1Jw8lyhiP6sN6Vr6GCIByePx9PFzaKjfGYV4Pz3lBxDc/edit?usp=drive_link"
    st.write("[Sponsorship List Spreadsheet](%s)" % url_spreadsheet, " (*update contact status and response from sponsor*)")
    url_email = "https://drive.google.com/file/d/1SEjxod6BeDbaYClsrgEDAu4mOt2ccIav/view?usp=sharing"
    st.write("[Sponsorship Email Guide](%s)" % url_email)
    url_packet = "https://drive.google.com/file/d/1bVNp_e8gIlc4jAdFwh50_MglCaGSeP7-/view?usp=sharing"
    st.write("[Sponsorship Packet](%s)" % url_packet)
    url_form = "https://drive.google.com/file/d/16uUChWPrWimHgDzBOtixHfX-9KLrYl-k/view?usp=sharing"
    st.write("[Editable Sponsorship & Donation Agreement Form](%s)" % url_form, " (*download and send to sponsor after receiving response*)")
    url_tax = "https://drive.google.com/file/d/1rGkPGP1Db8tEafDXQKNc6aOzbD70Rhx-/view?usp=sharing"
    st.write("[Tax Exemption Form](%s)" % url_tax)

# Google Sheets URL
url = "https://docs.google.com/spreadsheets/d/1HNXsI2Ic735AwpMVuKrGS93OOSxWMUU37W5zQSe-Bis/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# Google Sheets dataframe
df_first = conn.read(spreadsheet=url, usecols=[1,2,6,7,8])

st.header("Sponsorship List")

# Display dataframe
st.dataframe(df_first)

# Google Sheets dataframe
df_second = conn.read(spreadsheet=url, usecols=list(range(11)))

# Convert latitude and longitude to floats
df_second["Latitude"] = df_second["Latitude"].astype(float)
df_second["Longitude"] = df_second["Longitude"].astype(float)

st.header("Locations Map")

# Initialize map center on mean coordinates
map_center = [df_second["Latitude"].mean(), df_second["Longitude"].mean()]
map = folium.Map(location=map_center)

# Add markers and pop-ups
for i in range(len(df_second["Company"])):
    # Define HTML content for popup and hover
    html = f"<b>{df_second['Company'][i]}</b><br><b>Address:</b> {df_second['Address'][i]}<br><b>Phone:</b> {df_second['Phone Number'][i]}"
    iframe = folium.IFrame(html=html, width=475, height=75)

    # Create markers with hover effect
    folium.Marker(
        location=[df_second["Latitude"][i], df_second["Longitude"][i]],
        popup=folium.Popup(iframe),
        tooltip=df_second["Company"][i],
        icon=folium.Icon(color='red', icon=None)
    ).add_to(map)

# Display map
st_folium.folium_static(map)

st.header("Sponsorship Assignments")

st.markdown(
    """
    Use the selection widget provided to choose your name from the list of ambassadors. After selecting your name, the application will display all sponsorship assignments associated with you. :star2: indicates that the company was a **previous** **sponsor/donor**. Use the following information to contact your assigned company sponsors.
    """
)

option = st.selectbox(
    "What is your name?",
    ("Emily", "Hana", "Lucie", "Makayla", "Martin", "Mckenzie", "Michael", "Nishka", "Preston", "Shivani"),
    index=None,
    placeholder="Select name..."
)

for i in range(len(df_second["Ambassador"])):
    if option == df_second["Ambassador"][i]:
        if df_second["Previous Donor/Sponsor?"][i] == "Y":
            st.subheader(f"{df_second['Company'][i]} :star2:")
        else:
            st.subheader(df_second["Company"][i])
        if pd.notna(df_second["Contact"][i]):
            st.write("- **Contact:** ", df_second["Contact"][i])
        if pd.notna(df_second["Email"][i]):
            st.write("- **Email:** ", df_second["Email"][i])
        if pd.notna(df_second["Phone Number"][i]):
            st.write("- **Phone:** ", df_second["Phone Number"][i])
        if pd.notna(df_second["Link"][i]):
            st.write("- **URL:** ", df_second["Link"][i])
        if pd.notna(df_second["Notes"][i]):
            st.write("- **Notes:** ", df_second["Notes"][i])