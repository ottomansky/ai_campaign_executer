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

# Minimalist CSS for a modern look and centered elements
st.markdown("""
    <style>
        /* Background and layout */
        body { background-color: #f8f9fa; }
        .css-1d391kg { max-width: 1200px; margin: auto; }
        .stApp { background-color: #f8f9fa; }
        
        /* Title and header */
        h1 { color: #4a4a4a; font-family: 'Segoe UI', sans-serif; font-weight: bold; text-align: center; margin-top: 10px; }
        
        /* Center table */
        .stDataFrameContainer {
            display: flex;
            justify-content: center;
        }

        /* Buttons */
        button { background-color: #4a90e2; color: white; border-radius: 5px; padding: 10px 20px; border: none; }
        button:hover { background-color: #357ab8; }
        
        /* Footer styling */
        footer { 
            visibility: visible; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 20px 40px; 
            background-color: #ffffff; 
            border-top: 1px solid #eaeaea;
            position: fixed;
            bottom: 0;
            width: 100%;
        }

        footer p { margin: 0; color: #4a4a4a; font-family: 'Segoe UI', sans-serif; }
        
        /* Hide default streamlit footer */
        .css-12oz5g7 { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Keboola credentials
token = st.secrets["kbc_token"]
url = st.secrets["kbc_url"]
client_upload = Client(url, token)

# Function to format phone numbers as plain text without commas and with better readability
def format_phone_number(number):
    if pd.isna(number):  # Check for NaN
        return number
    number = str(int(number))  # Convert to int first to remove decimals
    return f"+{number[:1]} {number[1:4]} {number[4:7]} {number[7:]}"  # Adjust the format based on your phone number style

# Main function
def main():
    # Set up Streamlit container with title and logo
    with st.container():
        st.markdown(f"""<div style="display: flex; justify-content: center;">
                        <img src="data:image/png;base64,{logo_base64}" style="width: 120px; margin-bottom: 20px;">
                        </div>""", unsafe_allow_html=True)
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
    if 'phone_number' in data.columns:
        data['phone_number'] = data['phone_number'].apply(format_phone_number)

    # Display the data in an editable table with horizontal scrolling enabled and centered
    st.markdown("<style>div[data-testid='stDataFrameContainer'] > div { overflow-x: auto; display: flex; justify-content: center; }</style>", unsafe_allow_html=True)
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

if __name__ == '__main__':
    main()

# Custom footer at the bottom of the page
st.markdown(f"""
<footer>
    <p><strong>Version:</strong> 1.1</p>
    <img src="data:image/png;base64,{logo_base64}" style="width: 100px;">
</footer>
""", unsafe_allow_html=True)
