import plotly.express as px
import streamlit as st

def create_prices(all_prices):
    st.markdown("## Price comparison")

    fig = px.line(
        all_prices,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (EUR/MWh)",
        legend_title_text="Commodity",
        hovermode="closest",
        dragmode=False,
    )
    fig.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig)