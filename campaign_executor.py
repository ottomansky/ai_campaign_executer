import streamlit as st
import pandas as pd
import os
from kbcstorage.client import Client

# Set Streamlit page config
st.set_page_config(page_title="GenAI Messaging Campaign", page_icon=":robot:", layout="wide")

# Keboola credentials
token = st.secrets["kbc_token"]
url = st.secrets["kbc_url"]
client_upload = Client(url, token)

# Main function
def main():
    # Set up Streamlit container with title and logo
    with st.container():
        st.title("Twilio Campaign Approval")

    file_path = "/data/in/tables/twilio_sms_campaign_approval_request.csv"

    # Read data from CSV
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        st.error("Oops! Couldn't find the data. 🤔")
        return

    # Display the data in an editable table with horizontal scrolling enabled
    st.markdown("<style>div[data-testid='stDataFrameContainer'] > div { overflow-x: auto; }</style>", unsafe_allow_html=True)
    
    edited_data = st.data_editor(data, num_rows="dynamic", width=2000, height=600)  # Increased width to 2000 for more space

    # Add a button for uploading the edited data
    if st.button("🚀 Upload to Keboola"):
        with st.spinner('Crafting the perfect AI-generated messages... your SMS campaign is loading 📲🤖'):
            try:
                # Remove previous file if it exists
                if os.path.exists('updated_data.csv.gz'):
                    os.remove('updated_data.csv.gz')

                # Save the edited data to a compressed CSV
                edited_data.to_csv('updated_data.csv.gz', index=False, compression='gzip')

                # Upload the file to Keboola
                client_upload.tables.load(
                    table_id='out.c-campaign-executer.twilio_sms_campaign_approval_request',
                    file_path='updated_data.csv.gz',
                    is_incremental=False
                )

                st.success("Your AI-driven SMS campaign is ready to send! 🚀📲")
            except Exception as e:
                st.error(f"Oops! Something went wrong while preparing the campaign: {e} 😬")

if __name__ == '__main__':
    main()
