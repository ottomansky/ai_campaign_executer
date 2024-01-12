from kbcstorage.client import Client
import streamlit as st
import pandas as pd
import csv
import os
from streamlit_option_menu import option_menu
import base64

logo_image = os.path.abspath("./app/static/keboola.png")

logo_html = f"""<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 100px; margin-left: -10px;"></div>"""
html_footer = f"""
 <div style="display: flex; justify-content: flex-end;margin-top: 12%">
        <div>
            <p><strong>Version:</strong> 1.1</p>
        </div>
        <div style="margin-left: auto;">
            <img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 100px;">
        </div>
    </div>
"""

token = st.secrets["kbc_storage_token"]
url = st.secrets["kbc_url"]

#st.set_page_config(layout="wide",)

client_upload = Client(url, token)

def main():

    # Set up Streamlit container with title and logo
    with st.container():
        st.markdown(f"{logo_html}", unsafe_allow_html=True)
        st.title("Twilio Campaign Approval")
    
    file_path = "/data/in/tables/twilio_sms_campaign_approval_request.csv"
    data = pd.read_csv(file_path)
    
    # Display the data in an editable table using st.data_editor
    edited_data = st.data_editor(data, num_rows="dynamic", width=1400, height=500)


    if st.button("Upload to Keboola"):
        if os.path.exists('updated_data.csv'):
            os.remove('updated_data.csv.gz')
        else:
            print("The file does not exist")
        
        edited_data.to_csv('updated_data.csv.gz', index=False,compression='gzip')
        
        client_upload.tables.load(table_id = 'out.c-campaign-executer.twilio_sms_campaign_approval_request' , file_path='updated_data.csv.gz', is_incremental=False)

    
    # Display HTML footer
    st.markdown(html_footer, unsafe_allow_html=True)

    # Hide Made with streamlit from footer
    hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
