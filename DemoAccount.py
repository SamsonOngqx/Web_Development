#Require pip install
from simple_salesforce import Salesforce
import pandas as pd
import smtplib
import streamlit as st
import plotly.express as px
import numpy as np

#Does not require pip install
import requests
from io import StringIO
from datetime import datetime, timedelta

st.set_page_config(page_title="RWS Incident Report",
                   page_icon=":book:",
                   layout="wide")

# Set up Salesforce credentials
username = 'sushantn.rven@rws.sg.partial'
password = 'Pune@123'
security_token = 'RVpnTZe6ebLS5jGFAtH47zQO8'


#username = 'samson.ongqx@rwsentosa.com'
#password = 'T0020261j!'
#security_token = '5poloGj35vQyuIxiHvnTmJoG'


# Instantiate the Salesforce client
sf = Salesforce(username=username, password=password, security_token=security_token, domain='test')

#Your Salesforce Instance URL
sf_instance = 'https://test.salesforce.com/'

#Querying for the incident reports
data = sf.query("SELECT  Owner.Name , BMCServiceDesk__Category_ID__c,Category_Tree__c, CauseCatTier1_AL__c, CauseCatTier2_AL__c,  custom_Client_Department__c, BMCServiceDesk__clientEmail__c, BMCServiceDesk__clientId__c , CustomAL_Client_Location__c , BMCServiceDesk__Client_Name__c , BMCServiceDesk__Client_Phone__c, BMCServiceDesk__Closed_By__c,BMCServiceDesk__closeDateTime__c, Contact_AL__c, Contact_VIP_Status__c , CustomAL_Description__c , CustomAL_First_Assignment_Date__c , BMCServiceDesk__firstCallResolution__c , BMCServiceDesk__clientFirstName__c,CustomAL_Service_Request_Number__c, BMCServiceDesk__clientLastName__c, CustomAL_Incident_Number__c ,BMCServiceDesk__openDateTime__c , Console_Potential_FCR_AL__c , CustomAL_Priority__c , BMCServiceDesk__incidentResolution__c , Resolved_Date_Time_AL__c , CustomWK_SDCases__c , CustomAL_SecInc__c , Source_AL__c , BMCServiceDesk__FKOpenBy__c , BMCServiceDesk__Status_ID__c , Summary__c , CustomAL_Ticket_Age__c , BMCServiceDesk__Type__c , 	CustomAL_Vendor_Ticket__c , BMCServiceDesk__VIP_Client__c , BMCServiceDesk__dueDateTime__c , BMCServiceDesk__timeSpent__c , BMCServiceDesk__TotalWorkTime__c , BMCServiceDesk__Total_Duration__c, BMCServiceDesk__state__c , BMCServiceDesk__Reassigned_Count__c , id , BMCServiceDesk__respondedDateTime__c , CustomAL_Scheduled_End_Date__c , name , BMCServiceDesk__Clock_Status__c , BMCServiceDesk__Queue__c , LastModifiedBy.Name  FROM BMCServiceDesk__Incident__c Where BMCServiceDesk__Type__c = 'Incident' AND BMCServiceDesk__state__c = True AND BMCServiceDesk__Status_ID__c != 'RESOLVED'")

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%dT%H:%M:%S.") + "{:03d}".format(current_time.microsecond // 1000) + "+0000"

df = pd.DataFrame(data['records'])
df = df.drop(columns = 'attributes')
df["diff_days"] = ((pd.to_datetime(df['Resolved_Date_Time_AL__c'])).fillna(current_date) - (pd.to_datetime(df['BMCServiceDesk__openDateTime__c']))) / np.timedelta64(1, 'D')

#df.to_csv("sf_data_demo.csv", index = False)


# ----SideBar ----

st.sidebar.header("Please Filter Here: ")
queue_type = st.sidebar.multiselect(
    "Select the Category: ",
    options = df["BMCServiceDesk__Category_ID__c"].unique(),
    default = df["BMCServiceDesk__Category_ID__c"].unique()
)


#department = st.sidebar.multiselect(
#    "Select the Category: ",
#    options = df["custom_Client_Department__c"].unique(),
#    default = df["custom_Client_Department__c"].unique()
#)

df_selection = df.query(
    "BMCServiceDesk__Category_ID__c == @queue_type"
)

st.dataframe(df_selection)

# ---- MainPage ----
st.title(":bar_chart: Tickets Dashboard")
st.markdown("###")

# TOP Incident Reports
total_incident = int(df_selection["BMCServiceDesk__Category_ID__c"].count())

# Number of Incident Lapsed
total_lapsed = len(df_selection[df_selection["diff_days"] > 5])

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Number Of Tickets:")
    st.subheader(f"{total_incident}")
with right_column:
    st.subheader("Total Number Of Tickets Lapsed")
    st.subheader(f"{total_lapsed}")

st.markdown("---")
