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

# Group the data by unique values in 'BMCServiceDesk__Category_ID__c'
grouped_data = df.groupby('BMCServiceDesk__Category_ID__c')

# Create the interactive dashboard
st.title(":bar_chart: Ticket Analysis Dashboard")

# Split the page into two columns
col1, col2 = st.columns(2)

# Create a container for the dashboard content in each column
with col1:
    dashboard_container1 = st.container()
with col2:
    dashboard_container2 = st.container()

# Display details for each category
for i, (category, category_data) in enumerate(grouped_data):
    # Calculate the counts for each category
    total_tickets = category_data.shape[0]
    tickets_within_3_to_5_days = category_data[
        (category_data['diff_days'] > 3) & (category_data['diff_days'] < 5)
    ].shape[0]
    tickets_lapsed = category_data[category_data['diff_days'] > 5].shape[0]

    # Display the counts in a row layout
    if i % 2 == 0:
        with dashboard_container1:
            st.header(f"{category}")
            col1_1, col1_2, col1_3 = st.columns(3)
            with col1_1:
                st.metric("Total Tickets", total_tickets)
            with col1_2:
                st.metric("Tickets within 3 to 5 days", tickets_within_3_to_5_days)
            with col1_3:
                st.metric("Tickets lapsed", tickets_lapsed)
            st.markdown("""<hr style='border: 1px solid #ccc'>""", unsafe_allow_html=True)
    else:
        with dashboard_container2:
            st.header(f"{category}")
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                st.metric("Total Tickets", total_tickets)
            with col2_2:
                st.metric("Tickets within 3 to 5 days", tickets_within_3_to_5_days)
            with col2_3:
                st.metric("Tickets lapsed", tickets_lapsed)
            st.markdown("""<hr style='border: 1px solid #ccc'>""", unsafe_allow_html=True)

# Apply styling to the dashboard
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .css-1uj3fd7 {
        border-left: 1px solid #ccc;
        margin-left: 1rem;
        margin-right: 1rem;
    }
    .css-1g1a6fx {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
