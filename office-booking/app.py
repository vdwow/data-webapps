import streamlit as st
import os
from dotenv import load_dotenv
import streamlit_google_oauth as oauth
from google.oauth2 import service_account

import collections.abc
#hyper needs the four following aliases to be done manually.
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping

from gsheetsdb import connect

load_dotenv()

client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]


if __name__ == "__main__":
    
    st.title('RHC Office Booking')
    
    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        login_button_text="Continue with Google",
        logout_button_text="Logout",
    )
    if login_info:
        user_id, user_email = login_info
        st.write(f"Welcome {user_email}")
        
        # Create a connection object.
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        
        conn = connect(credentials=credentials)

        # Perform SQL query on the Google Sheet.
        # Uses st.cache to only rerun when the query changes or after 10 min.
        @st.cache(ttl=600)
        
        def run_query(query):
            rows = conn.execute(query, headers=1)
            rows = rows.fetchall()
            return rows

        sheet_url = st.secrets["private_gsheets_url"]
        rows = run_query(f'SELECT * FROM "{sheet_url}"')

        # Print results.
        for row in rows:
            st.write(f"{row.name} has a :{row.pet}:")
        
    else:
        st.write("Please login")