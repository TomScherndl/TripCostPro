import logging
from code.entsoe_download import load_data_from_entsoe  
from matplotlib import pyplot as plt
import streamlit as st

def main(download_data:bool=True):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dashboard!")

    if download_data:
        data = load_data_from_entsoe()
        logging.info("Data downloaded successfully.")

    st.markdown("# Dashboard Content")
    st.line_chart(data)
    plt.show()

if __name__ == "__main__":
    main()
