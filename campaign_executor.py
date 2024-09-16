import streamlit as st
import pandas as pd
import os
import base64
from kbcstorage.client import Client

# Set Streamlit page config
st.set_page_config(page_title="GenAI Messaging Campaign", page_icon=":robot:", layout="wide")

# Function to load the logo and convert it to base64
def load_logo(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

# Keboola logo
logo_image_path = os.path.abspath("./app/static/keboola.png")
logo_base64 = load_logo(logo_image_path)

# HTML for logo at the top and bottom
logo_html = f"""<div style="display: flex; justify-content: flex-end;">
<img src="data:image/png;base64,{logo_base64}" style="width: 100px; margin-left: -10px;"></div>"""
html_footer = f"""
 <div style="display: flex; justify-content: flex-end;margin-top: 12%">
        <div>
            <p><strong>Version:</strong> 1.1</p>
        </div>
        <div style="margin-left: auto;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 100px;">
        </div>
    </div>
"""

# Keboola credentials
token = st.secrets["kbc_token"]
url = st.secrets["kbc_url"]
client_upload = Client(url, token)

# Function to format phone numbers as plain text without commas
def format_phone_number(number):
    if pd.isna(number):  # Check for NaN
        return number
    number = str(int(number))  # Convert to int first to remove decimals
    return f"+{number}"

# Main function
def main():
    # Set up Streamlit container with title and logo
    with st.container():
        st.markdown(f"{logo_html}", unsafe_allow_html=True)
        st.title("Twilio Campaign Approval")

    # File path
    file_path = "/data/in/tables/twilio_sms_campaign_approval_request.csv"

    # Check if file exists and read data
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        st.error("Oops! Couldn't find the data. 🤔")
        return

    # Format the phone number column if it exists
    if 'Phone Number' in data.columns:
        data['Phone Number'] = data['Phone Number'].apply(format_phone_number)

    # Display the data in an editable table with horizontal scrolling enabled
    st.markdown("<style>div[data-testid='stDataFrameContainer'] > div { overflow-x: auto; }</style>", unsafe_allow_html=True)
    edited_data = st.data_editor(data, num_rows="dynamic", width=1400, height=500)

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

    # Display HTML footer
    st.markdown(html_footer, unsafe_allow_html=True)

    # Hide Streamlit footer
    hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
