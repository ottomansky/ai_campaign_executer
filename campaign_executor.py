from kbcstorage.client import Client
import streamlit as st
import pandas as pd
import csv
import os
from streamlit_option_menu import option_menu


token = st.secrets["kbc_bucket_token"]

st.set_page_config(
    
    layout="wide",
    
)



client_upload = Client('https://connection.north-europe.azure.keboola.com', token)

def main():


    st.title("APP: Twilio campaing approval")

    data = pd.read_csv('/data/in/tables/twilio_sms_campaign_approval_request.csv')
    # Display the data in an editable table using st.data_editor
    edited_data = st.data_editor(data, num_rows="dynamic", width=1400, height=500)


    if st.button("Send to Keboola"):
        if os.path.exists('updated_data.csv'):
            os.remove('updated_data.csv.gz')
        else:
            print("The file does not exist")
        
        edited_data.to_csv('updated_data.csv.gz', index=False,compression='gzip')
        
        client_upload.tables.load(table_id = 'out.c-twillio-sms-data-preparation.twilio_sms_campaign_approval_request' , file_path='updated_data.csv.gz', is_incremental=False)
if __name__ == '__main__':
    main()
