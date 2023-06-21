import pandas as pd
import streamlit as st

# Load the data from the CSV file
data_url = "https://raw.githubusercontent.com/SamsonOngqx/Web_Development/main/sf_data_with_new_Date.csv"
df = pd.read_csv(data_url)

# Group the data by unique values in 'BMCServiceDesk__Category_ID__c'
grouped_data = df.groupby('BMCServiceDesk__Category_ID__c')

# Set page configuration
st.set_page_config(layout="wide")

# Create the interactive dashboard
st.title("Ticket Analysis Dashboard")

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
            # Create an expander for the category
            expander = st.expander(f"{category}", expanded=False)

            # Add a selectbox to choose the ticket header
            ticket_header = expander.selectbox(
                "Select Ticket Header",
                options=["Total Tickets", "Tickets within 3 to 5 days", "Tickets lapsed"],
                key=f"selectbox_{category}"
            )

            # Filter the data based on the selected ticket header
            if ticket_header == "Total Tickets":
                filtered_data = category_data
            elif ticket_header == "Tickets within 3 to 5 days":
                filtered_data = category_data[
                    (category_data['diff_days'] > 3) & (category_data['diff_days'] < 5)
                ]
            else:
                filtered_data = category_data[category_data['diff_days'] > 5]

            # Display the filtered dataframe
            if expander.button("Show Dataframe", key=f"button_{category}"):
                with st.expander("Expanded Dataframe", expanded=True):
                    st.dataframe(filtered_data, height=800)

            col1_1, col1_2, col1_3 = expander.columns(3)
            with col1_1:
                st.metric("Total Tickets", total_tickets)
            with col1_2:
                st.metric("Tickets within 3 to 5 days", tickets_within_3_to_5_days)
            with col1_3:
                st.metric("Tickets lapsed", tickets_lapsed)
            st.markdown("""<hr style='border: 1px solid #ccc'>""", unsafe_allow_html=True)
    else:
        with dashboard_container2:
            # Create an expander for the category
            expander = st.expander(f"{category}", expanded=False)

            # Add a selectbox to choose the ticket header
            ticket_header = expander.selectbox(
                "Select Ticket Header",
                options=["Total Tickets", "Tickets within 3 to 5 days", "Tickets lapsed"],
                key=f"selectbox_{category}"
            )

            # Filter the data based on the selected ticket header
            if ticket_header == "Total Tickets":
                filtered_data = category_data
            elif ticket_header == "Tickets within 3 to 5 days":
                filtered_data = category_data[
                    (category_data['diff_days'] > 3) & (category_data['diff_days'] < 5)
                ]
            else:
                filtered_data = category_data[category_data['diff_days'] > 5]

            # Display the filtered dataframe
            if expander.button("Show Dataframe", key=f"button_{category}"):
                with st.expander("Expanded Dataframe", expanded=True):
                    st.dataframe(filtered_data, height=800)

            col2_1, col2_2, col2_3 = expander.columns(3)
            with col2_1:
                st.metric("Total Tickets", total_tickets)
            with col2_2:
                st.metric("Tickets within 3 to 5 days", tickets_within_3_to_5_days)
            with col2_3:
                st.metric("Tickets lapsed", tickets_lapsed)
            st.markdown("""<hr style='border: 1px solid #ccc'>""", unsafe_allow_html=True)

# Apply styling to the dashboard
dashboard_container1.markdown(
    """
    <style>
    .css-1uj3fd7 {
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
dashboard_container2.markdown(
    """
    <style>
    .css-1uj3fd7 {
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
