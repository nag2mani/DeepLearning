import streamlit as st

if st.checkbox("Show / Hide"):
    st.text("Showing or Hiding widget")


# Radio Buttons
status = st.radio("What is your Status", ("Active", "Inactive"))


# Status checking
if status == "Active":
    st.success("You are Active")


# If else status
if status == "Active":
    st.success("You are Active")
else:
    st.warning("You are inactive, Please activate it")


# SelectBox
occupation = st.selectbox("Your Occupation", ["Programmer", "Data Scientist", "Docter", "Businessman"])
st.write("You Selected this option", occupation)

location = st.multiselect("Where do you work", ("Karnatka", "Mumbai", 
"Pune", "Delhi"))


# Counting Location
st.write("You Selected", len(location), "locations")


# Slider
lelvel = st.slider("Your level is ", 1,5)


# Buttons
st.button("Simple Button")
if st.button("About"):
    st.text("Streamlit is cool")

if st.button("Submit"):
    st.text("Sucessful Submited")


# text Input
first_name = st.text_input("Enter your first name", "Type here..")
if st.button("Submit", key="1"):
    result = first_name.title()
    st.success(result)


# Text Area
message = st.text_area("Enter your message", "Type here..")
if st.button("Submit", key = "2"):
    result = message.title()
    st.success(result)


# Date Input
import datetime
today = st.date_input("Today is", datetime.datetime.now())


# Time
the_time = st.time_input("The time is", datetime.time())


#Display Json Output
st.text("Display json Data")
st.json({"Name":"Nagmani",
        "Gender":"Male"})


# code with copy icon
st.text("Display Row Code")
st.code("import numpy as np")


# Code with multiple line
with st.echo():
    import pandas as pd
    df = pd.DataFrame()


# Progress bar
import time
my_bar = st.progress(0)
for p in range(10):
    my_bar.progress( p + 10)


#spinner
with st.spinner("Watinig .."):
    time.sleep(5)
st.success("Finished!")


# ballon
st.title("Happy Birday!")
st.balloons()


# Sidebar
st.sidebar.header("About")
st.sidebar.text("This is our demo project")


# Select Box
algoritmhs = st.sidebar.selectbox("Your Algorithm", ["Liner Regression", "Logistic Regression", "Decision tree",
"Random Forest"])



