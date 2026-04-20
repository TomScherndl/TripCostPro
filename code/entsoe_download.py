from entsoe import EntsoePandasClient
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st

@st.cache_data
def load_data_from_entsoe(country_code = 'AT', 
                          start = pd.Timestamp('20241201', tz='Europe/Brussels'), 
                          end = pd.Timestamp('20250101', tz='Europe/Brussels')): 
    load_dotenv()
    client = EntsoePandasClient(api_key=os.getenv("ENTSOE_API_TOKEN"))

    # start = pd.Timestamp('20171201', tz='Europe/Brussels')
    # end = pd.Timestamp('20180101', tz='Europe/Brussels')
    # country_code = 'AT'  # Austria
    # country_code_from = 'FR'  # France
    # country_code_to = 'DE_LU' # Germany-Luxembourg
    # type_marketagreement_type = 'A01'
    # contract_marketagreement_type = 'A01'
    # process_type = 'A51'

    # for all methods see https://github.com/EnergieID/entsoe-py; idea: 
    # ==> use registry to call methods dynamically
    data = client.query_day_ahead_prices(country_code, start=start, end=end)
    return data
